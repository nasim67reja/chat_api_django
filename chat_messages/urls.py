from django.urls import path
from .api_views import SendMessageView, MessageListView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('messages/', MessageListView.as_view(), name='message_list'),
]
