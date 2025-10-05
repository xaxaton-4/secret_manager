from django.urls import path


from openbao import api


urlpatterns = [
    path('secrets/create/', api.SecretCreate.as_view()),
    path('secrets/detail/', api.SecretDetail.as_view()),
]
