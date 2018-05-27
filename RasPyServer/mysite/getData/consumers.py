from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import os
import re
import subprocess
from django.conf import settings


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.previous_image =0

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        box_nr =  text_data_json['box_ID']
        imgF = os.path.join(settings.MEDIA_ROOT,'media','box_'+str(box_nr))
        #print(imgF)
        fs = [i for i in os.listdir(imgF) if 'j' in i]
        image_store = sorted(fs,key = lambda x: int(re.findall(r".*([0-9]+).*",x)[0]))
        nIms = len(image_store)
        previous_image = text_data_json['message']
        cIm = text_data_json['message']
        if len(image_store)>0:

            if image_store[-1] != previous_image:
                #os.remove(os.path.join(imgF,previous_image))
                #subprocess.run(["rm", os.path.join(imgF,previous_image)], shell=1)

                message = (int(text_data_json['message']) + 1) % 60

                #if (message-nIms)>10:
                #    message = nIms - 5

                img_loc = image_store[message]

                await self.send(text_data=json.dumps({
                    'message': message,
                    'img_loc': img_loc
                }))
                self.previous_image=img_loc
            else:
                pass
        else:
            pass
