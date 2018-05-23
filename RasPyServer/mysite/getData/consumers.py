from channels.generic.websocket import WebsocketConsumer
import json
import os

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        imgF = '/Users/Yves/Documents/Code/behaviour_webserver/RasPyServer/mysite/getData/static/getData/ims/'
        image_store = sorted(os.listdir(imgF))
        text_data_json = json.loads(text_data)
        message = (int(text_data_json['message']) + 1) % 60
        try:
            img_loc = image_store[message]


            self.send(text_data=json.dumps({
                'message': message,
                'img_loc': img_loc
            }))
        except:
            pass
