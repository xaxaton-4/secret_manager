import requests

from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class BaseApiView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # logging here?
        return super().dispatch(request, *args, **kwargs)


class EmailSenderMixin:
    def send_email_to_admins(self, title: str, template: str, message: str):
        for user in User.objects.filter(is_superuser=True):
            try:
                self.send_email(title, template, user.email, message)
            except Exception:
                # put log here
                pass

    def send_email(self, title: str, template: str, email: str, message: str):
        context = {'message': message}
        prepared_message = render_to_string(template, context)
        email = EmailMessage(title, prepared_message, to=(email,))
        email.content_subtype = 'html'
        email.send()


class NotificationsMixin:
    def send_notif_to_admins(self, message: str):
        for user in User.objects.filter(is_superuser=True):
            try:
                self.send_notif(user.pk, message)
            except Exception:
                # put log here
                pass

    def send_notif(self, user_id: int, message: str):
        data = {'command': 'notify', 'message': message}
        try:
            requests.post(f'{settings.NOTIFY_SERVICE_URL}/notify/send?account_id={user_id}', data=data)
            return True
        except Exception:
            return False
