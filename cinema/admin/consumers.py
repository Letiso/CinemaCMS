from channels.generic.websocket import AsyncWebsocketConsumer


class MailingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('mailing', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('mailing', self.channel_name)

    async def send_progress(self, event):
        text_message = event['text']

        await self.send(text_message)
