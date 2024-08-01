from django.urls import re_path
from . import consumers  # Make sure to import your consumer class

websocket_urlpatterns = [
    re_path(r'ws/notify/$', consumers.NotifyConsumer.as_asgi()),
]