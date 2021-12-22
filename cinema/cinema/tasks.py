# from time import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from cinema.celery import app

channel_layer = get_channel_layer()


@app.task
def hello_world():
    # sleep(5)
    string = 'Hello World'
    print(string)
    async_to_sync(channel_layer.group_send)('mailing', {'type': 'send_progress', 'text': string})
