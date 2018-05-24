from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asychio
import os

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):

        while True:
            await asyncio.sleep(0.1)
            imgF = '/Users/Yves/Documents/Code/behaviour_webserver/RasPyServer/mysite/getData/static/getData/ims/'
            image_store = sorted(os.listdir(imgF))
            text_data_json = json.loads(text_data)
            message = (int(text_data_json['message']) + 1) % 60
            try:
                img_loc = image_store[message]


                await self.send(text_data=json.dumps({
                    'message': message,
                    'img_loc': img_loc
                }))
            except:
                pass
