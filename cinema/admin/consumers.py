from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    group = None

    async def connect(self):
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, *args, **kwargs):
        await self.channel_layer.group_discard(self.group, self.channel_name)


# region Mailing
class MailingConsumer(Consumer):
    async def send_progress(self, event):
        text_message = event['text']
        await self.send(text_message)


class SMSConsumer(MailingConsumer):
    group = 'SMS-mailing'


class EmailConsumer(MailingConsumer):
    group = 'email-mailing'


# endregion Mailing

# region MovieSession
class TicketBookingCancelConsumer(Consumer):
    group = 'disable-tickets'


class TicketBookingConsumer(Consumer):
    group = 'enable-tickets'

    async def send_tickets_to_enable(self, event):
        tickets_id_array = event['text']
        await self.send(tickets_id_array)

# endregion MovieSession
