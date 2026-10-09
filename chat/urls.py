from django.urls import path
from .views import ChatListAPIView, MessageCreateAPIView, ChatMessages, MessageEditAPIView


urlpatterns = [
    path('chat-list', ChatListAPIView.as_view()),
    path('message', MessageCreateAPIView.as_view()),
    path('chat-messages/<uuid:pk>', ChatMessages.as_view()),
    path('message/<uuid:pk>', MessageEditAPIView.as_view()),
]