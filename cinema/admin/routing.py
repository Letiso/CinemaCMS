from django.urls import path

from .consumers import SMSConsumer, EmailConsumer

ws_urlpatterns = [
    path('ws/SMS-mailing/', SMSConsumer.as_asgi()),
    path('ws/email-mailing/', EmailConsumer.as_asgi())
]
