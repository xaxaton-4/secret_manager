from rest_framework.views import APIView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.response import Response


class BaseApiView(APIView):
    def dispatch(self, request, *args, **kwargs):
        # logging here?
        return super().dispatch(request, *args, **kwargs)
    def success(self, data, status=200):
        return Response({"status": "success", "data": data}, status=status)

    def error(self, message, status=400):
        return Response({"status": "error", "message": message}, status=status)


class EmailSenderMixin:
    def send_email(self, title: str, template: str, email: str, message: str):
        context = {'message': message}
        prepared_message = render_to_string(template, context)
        email = EmailMessage(title, prepared_message, to=(email,))
        email.content_subtype = 'html'
        email.send()
