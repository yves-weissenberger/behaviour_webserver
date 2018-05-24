from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import os
import re
import subprocess

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.previous_image =0

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):

        imgF = '/Users/Yves/Documents/Code/behaviour_webserver/RasPyServer/mysite/getData/static/getData/ims/'
        fs = [i for i in os.listdir(imgF) if 'j' in i]
        image_store = sorted(fs,key = lambda x: int(re.findall(r"^([0-9]+).*",x)[0]))
        text_data_json = json.loads(text_data)
        previous_image = text_data_json['message']

        if len(image_store)>0:

            if image_store[-1] != previous_image:
                #os.remove(os.path.join(imgF,previous_image))
                #subprocess.run(["rm", os.path.join(imgF,previous_image)], shell=1)

                message = text_data_json['message']
                print (previous_image)

                img_loc = image_store[-1]

                await self.send(text_data=json.dumps({
                    'message': img_loc,
                    'img_loc': img_loc
                }))
                self.previous_image=img_loc
            else:
                pass
        else:
            pass
