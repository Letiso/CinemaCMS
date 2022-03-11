from django.urls import path

from .consumers import SMSConsumer, EmailConsumer, TicketBookingCancelConsumer, TicketBookingConsumer

ws_urlpatterns = [
    path('ws/SMS-mailing/', SMSConsumer.as_asgi()),
    path('ws/email-mailing/', EmailConsumer.as_asgi()),
    path('ws/disable-tickets/', TicketBookingCancelConsumer.as_asgi()),
    path('ws/enable-tickets/', TicketBookingConsumer.as_asgi())
]
