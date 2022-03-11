import json
from math import floor
from time import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from cinema.celery import app

CHANNEL_LAYER = get_channel_layer()


# region Mailing
def send_email(message, user):
    email = EmailMultiAlternatives('Рассылка от CinemaCMS', message, settings.EMAIL_HOST_USER, [user.email])
    email.attach_alternative(message, 'text/html')
    email.send()


MAILING_SERVICES = {
    'SMS': lambda message, user: None,
    'email': lambda message, user: send_email(message, user),
}


@app.task
def send_mail(prefix, message, receivers_filter):
    mailing_receivers = get_user_model().objects.filter(**receivers_filter)
    receivers_count = len(mailing_receivers)
    prev_progress = mails_sent = 0

    for user in mailing_receivers:
        MAILING_SERVICES[prefix](message, user)
        mails_sent += 1
        progress = floor((mails_sent / receivers_count) * 100)

        if progress != prev_progress:
            prev_progress = progress
            async_to_sync(CHANNEL_LAYER.group_send)(
                f'{prefix}-mailing', {'type': 'send_progress', 'text': str(progress)}
            )


# endregion Mailing

# region MovieSession
@app.task
def cancel_ticket_booking():
    pass


@app.task
def update_ticket_booking_show(tickets):
    async_to_sync(CHANNEL_LAYER.group_send)(
        'enable-tickets', {'type': 'send_tickets_to_enable', 'text': json.dumps(tickets)}
    )



# endregion MovieSession
