from channels.generic.websocket import AsyncWebsocketConsumer

import json
class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']

        self.room_group_name = "chat_%s" % self.room_name

        # ADding the user to the Group.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg = text_data_json['message']
        user = text_data_json['username']
        print(msg)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg,
                "user": user,
            }
        )

    async def chat_message(self, event):
        msg = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            "message": msg,
            "user": user,
        }))