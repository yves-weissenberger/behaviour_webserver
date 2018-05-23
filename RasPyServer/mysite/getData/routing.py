# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/getData/(?P<box_nr>[0-9]+)/$', consumers.ChatConsumer),
]
