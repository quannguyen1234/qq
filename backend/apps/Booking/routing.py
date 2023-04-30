from django.urls import path
from .consumers import Conversation,ChatConsumer


channel_routing = [
    # path('booking/doctor/receive-order', ReceiveOrderDoctor.as_asgi()),
    path('booking/conversation/<str:access>', Conversation.as_asgi()),
    path('booking/cc/<str:access>',ChatConsumer.as_asgi()),
]