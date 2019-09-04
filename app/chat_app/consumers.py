import asyncio
import json
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Thread, ChatMessage


class ChatConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        receiver = self.scope['url_route']['kwargs']['username']
        sender = self.scope['user']
        self.thread_obj = await self.get_thread(sender, receiver)
        self.chat_room = f'thread_{self.thread_obj.id}'
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name)
        await self.send({
            'type': 'websocket.accept',
        })

    async def websocket_receive(self, event):
        # Reveiving json as a raw string
        data_string_format = event.get('text', None)
        if data_string_format is not None:
            # Converting string to dict
            data_dict_format = json.loads(data_string_format)
            msg = data_dict_format.get('msg')
            await self.create_new_message(msg)
            new_event = {
                'type': 'process_chat_message',
                'text': json.dumps({
                    'msg': msg,
                    'user': self.scope['user'].username,
                    'time': now().strftime("%b. %d, %Y, %I:%M %p"),
                })
            }
            await self.channel_layer.group_send(
                self.chat_room,
                new_event,
            )

    async def process_chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
        pass

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_thread(self, receiver, sender_username):
        return Thread.objects.get_or_new(receiver, sender_username)[0]

    @database_sync_to_async
    def create_new_message(self, message):
        return ChatMessage.objects.create(user=self.scope['user'], message=message, thread=self.thread_obj)

