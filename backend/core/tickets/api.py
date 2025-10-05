from django.core.paginator import Paginator
from rest_framework import status as status_code
from rest_framework.response import Response

from secrets_api.base_api import BaseApiView, EmailSenderMixin
from tickets.models import Ticket
from tickets.serializers import TicketSerializer, TicketCreateSerializer
from users.decorators import with_authorization, only_admin
from openbao.client import get_client


"""
@api {POST} /api/tickets/create/ CreateTicket
@apiGroup Ticket

@apiBody {String} resource Секрет, доступ к которому необходимо получить.
@apiBody {String} reason Причина запроса доступа.
@apiBody {Date} period Дата, до которой необходимо выдать ключ.

@apiSuccess (Ответ) {Number} id Идентификатор созданного тикета.
@apiSuccess (Ответ) {Boolean} with_email Было отправлено сообщение на почту.
"""
class CreateTicket(BaseApiView, EmailSenderMixin):
    @with_authorization
    def post(self, request):
        data = request.data
        data.update(user=request.user.pk)
        serializer = TicketCreateSerializer(data=data)
        if serializer.is_valid():
            new_ticket = serializer.save()
            email = request.user.email
            with_email = False
            if email:
                message = (
                    f'Ключ "{request.data["resource"]}" запрашивается до '
                    f'{request.data["period"]} в целях: "{request.data["reason"]}" '
                    f'пользователем {request.user.email}'
                )
                try:
                    self.send_email('Заявка на получение доступа', 'ticket.html', email, message)
                    with_email = True
                except Exception:
                    with_email = False
            return Response({'id': new_ticket.id, 'with_email': with_email})
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)


"""
@api {POST} /api/tickets/delete/ DeleteTicket
@apiGroup Ticket

@apiBody {Number} ticket_id Идентификатор тикета.
@apiBody {String} reason Причина отклонения тикета.
@apiBody {Boolean} force По умолчанию False. Если сообщение не было доставлено пользователю ни на почту, ни уведомлением, то тикет всё равно будет удален (при True).
"""
class DeleteTicket(BaseApiView, EmailSenderMixin):
    @only_admin
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        reason = request.data.get('reason', 'Не указана.')
        force = request.data.get('force', False)
        ticket = Ticket.objects.select_related('user').filter(pk=ticket_id)
        if not ticket.exists():
            return Response('There are no tickets with this id', status=status_code.HTTP_404_NOT_FOUND)

        t = ticket.first()
        email = t.user.email
        with_email = False

        if email:
            message = f'Ваш запрос на ключ "{t.resource}" отклонен. Причина: {reason}'
            try:
                self.send_email('Заявка на ключ отклонена.', 'ticket_not_approved.html', email, message)
                with_email = True
            except Exception:
                with_email = False

        # send notif
        notif_sended = True
        if notif_sended or with_email or force:
            t.delete()
            return Response(status=200)
        return Response(
            'Could not send feedback, if you still want to delete this ticket use "force" parameter',
            status=status_code.HTTP_400_BAD_REQUEST
        )


"""
@api {POST} /api/tickets/modify/ ModifyTicket
@apiGroup Ticket

@apiBody {Number} ticket_id Идентификатор тикета.
@apiBody {Boolean} is_approved Статус тикета.
@apiBody {Boolean} send_mail Отправить письмо пользователю. По умолчанию: True.

@apiSuccess (Ответ) {Number} id Идентификатор созданного тикета.
"""
class ModifyTicket(BaseApiView, EmailSenderMixin):
    @only_admin
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        new_status = request.data.get('is_approved')
        send_mail = request.data.get('send_mail', True)
        if ticket_id is None or new_status is None:
            return Response('ticket_id or is_approved missed', status=status_code.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.select_related('user').filter(pk=ticket_id)
        if not ticket.exists():
            return Response('ticket with this id doesnt exist', status=status_code.HTTP_400_BAD_REQUEST)
        t = ticket.first()
        t.is_approved = new_status
        with_email = False
        if send_mail:
            try:
                email = t.user.email
                self.send_email('Ключ выдан!', 'ticket.html', email, f'Доступ к ресурсу: "{t.resource}" выдан!')
                with_email = True
            except Exception:
                with_email = False
        t.save(update_fields=['is_approved'])
        openbao = get_client()
        openbao.share_to_user(t.user.pk, t.resource)
        return Response({'id': t.pk, 'with_email': with_email})


"""
@api {GET} /api/tickets/list/ TicketList
@apiGroup Ticket

@apiParam {Number} page Текущая страница списка тикетов.
@apiParam {Number} limit По умолчанию 150. Количество возвращаемых тикетов.

@apiSuccess (Ответ) {Object} ticket Тикет.
@apiSuccess (Ответ) {Number} ticket.id Идентификатор тикета.
@apiSuccess (Ответ) {String} ticket.resource Запрашиваемый секрет.
@apiSuccess (Ответ) {String} ticket.reason Причина запроса секрета.
@apiSuccess (Ответ) {Date} ticket.period Дата, до которой запрашивается секрет.
@apiSuccess (Ответ) {Boolean} ticket.is_approved Статус доступности секрета по тикету.
@apiSuccess (Ответ) {Object} ticket.user Пользователь, запросивший тикет.
@apiSuccess (Ответ) {Number} ticket.user.id Идентификатор пользователя.
@apiSuccess (Ответ) {String} ticket.user.email Электронная почта пользователя.
@apiSuccess (Ответ) {Date} ticket.user.date_joined Дата регистрации аккаунта.
@apiSuccess (Ответ) {Boolean} ticket.user.is_superuser Статус администратора.
@apiSuccess (Ответ) {Boolean} ticket.user.is_active Статус активности.
"""
class TicketsList(BaseApiView):
    @only_admin
    def get(self, request):
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 150)

        tickets_page = Paginator(Ticket.objects.all().order_by('id'), limit)
        tickets = [
            TicketSerializer(ticket).data
            for ticket in tickets_page.page(page)
        ]
        return Response(tickets)
