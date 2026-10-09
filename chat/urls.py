from django.urls import path
from .views import ChatListAPIView, MessageAPIView


urlpatterns = [
    path('chat-list', ChatListAPIView.as_view()),
    path('message', MessageAPIView.as_view()),
]