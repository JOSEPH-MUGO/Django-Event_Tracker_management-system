import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the WebSocket group
        await self.channel_layer.group_add(
            "public_room",  # Group name
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the WebSocket group
        await self.channel_layer.group_discard(
            "public_room",
            self.channel_name
        )

    async def send_notification(self, event):
        # Send message to WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))