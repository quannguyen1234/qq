from django.urls import path
from .consumers import Conversation


channel_routing = [
    # path('booking/doctor/receive-order', ReceiveOrderDoctor.as_asgi()),
    path('booking/conversation', Conversation.as_asgi()),
]