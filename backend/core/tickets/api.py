import datetime

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status as status_code
from rest_framework.response import Response

from secrets_api.base_api import BaseApiView
from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from users.decorators import with_authorization, only_admin


class CreateTicket(BaseApiView):
    @with_authorization
    def post(self, request):
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

        data = request.data
        data.update(user=request.user.pk)
        serializer = TicketSerializer(data=data)
        if serializer.is_valid():
            new_ticket = serializer.save()
            return Response({'id': new_ticket.id, 'with_email': with_email})
        return Response(serializer.errors, status=status_code.HTTP_400_BAD_REQUEST)

    def send_email(self, email: str, message: str):
        mail_subject = 'Заявка на получение доступа'
        context = {'message': message}
        prepared_message = render_to_string('ticket.html', context)
        email = EmailMessage(mail_subject, prepared_message, to=(email,))
        email.content_subtype = 'html'
        email.send()


class TicketsList(BaseApiView):
    @only_admin
    def get(self, request):
        tickets_qs = Ticket.objects.filter(is_approved=False, period__gte=datetime.datetime.now())
        tickets = [
            TicketSerializer(ticket).data
            for ticket in tickets_qs
        ]
        return Response(tickets)
