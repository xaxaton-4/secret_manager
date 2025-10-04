from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status as status_code
from rest_framework.response import Response

from secrets_api.base_api import BaseApiView
from tickets.models import Ticket
from tickets.serializers import TicketSerializer, TicketCreateSerializer
from users.decorators import with_authorization, only_admin


class CreateTicket(BaseApiView):
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
                    self.send_email(email, message)
                    with_email = True
                except Exception:
                    with_email = False
            return Response({'id': new_ticket.id, 'with_email': with_email})
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)

    def send_email(self, email: str, message: str):
        mail_subject = 'Заявка на получение доступа'
        context = {'message': message}
        prepared_message = render_to_string('ticket.html', context)
        email = EmailMessage(mail_subject, prepared_message, to=(email,))
        email.content_subtype = 'html'
        email.send()


class ModifyTicket(BaseApiView):
    @only_admin
    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        new_status = request.data.get('is_approved')
        if ticket_id is None or new_status is None:
            return Response('ticket_id or is_approved missed', status=status_code.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.filter(pk=ticket_id)
        if not ticket.exists():
            return Response('ticket with this id doesnt exist', status=status_code.HTTP_400_BAD_REQUEST)
        t = ticket.first()
        t.is_approved = new_status
        t.save(update_fields=['is_approved'])
        return Response({'id': t.pk})


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
