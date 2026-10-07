from django.urls import path
from .views import ChatListAPIView


urlpatterns = [
    path('chat-list', ChatListAPIView.as_view())
]