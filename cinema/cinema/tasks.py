from django.contrib.auth import get_user_model
from django.core.mail import send_mail as send_email
from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from cinema.celery import app

from time import sleep
from math import floor

CHANNEL_LAYER = get_channel_layer()

MAILING_SERVICES = {
    # 'SMS': lambda message, user: None,
    'SMS': lambda message, user: send_email(subject='Рассылка от CinemaCMS',
                                            message=message,
                                            from_email=settings.DEFAULT_FROM_EMAIL,
                                            recipient_list=[user.email]),
}


@app.task
def send_mail(prefix, message, receivers_filter):
    sleep(3)
    mailing_receivers = get_user_model().objects.filter(**receivers_filter)

    receivers_count = len(mailing_receivers)
    prev_progress = mails_sent = 0

    for user in mailing_receivers:
        MAILING_SERVICES[prefix](message, user)
        mails_sent += 1

        progress = floor((mails_sent / receivers_count) * 100)
        if progress != prev_progress:
            prev_progress = progress
            async_to_sync(CHANNEL_LAYER.group_send)(f'{prefix}-mailing', {
                'type': 'send_progress', 'text': str(progress)
            })
