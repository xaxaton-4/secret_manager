from django.urls import path


from tickets import api


urlpatterns = [
    path('tickets/list/', api.TicketsList.as_view()),
    path('tickets/create/', api.CreateTicket.as_view()),
]
