from django.urls import path

from .consumers import MailingConsumer

ws_urlpatterns = [
    path('ws/mailing/', MailingConsumer.as_asgi())
]
