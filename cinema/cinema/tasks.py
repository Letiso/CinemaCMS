from time import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from cinema.celery import app

channel_layer = get_channel_layer()


@app.task
def hello_world(prefix):
    for i in range(0, 101, 2):
        sleep(0.05)
        async_to_sync(channel_layer.group_send)(f'{prefix}-mailing', {'type': 'send_progress', 'text': str(i)})
