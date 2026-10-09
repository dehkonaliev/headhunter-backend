from .models import Chat, Message
from authentication.models import CustomUser
from .serializers import ChatSerializer, MessageSerializer, ChatMiniEmployeeSerializer, MessageSendSerializer
from baseapp.utils import success_response, error_response
from baseapp.permissions import IsEmployeeStrict, IsEmployer, IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ChatListAPIView(APIView):
    permission_classes = [IsEmployeeStrict]
    def get(self, request):
        chats = Chat.objects.filter(employee=request.user)
        
        return success_response(message="Chats list", data=ChatMiniEmployeeSerializer(chats, many=True).data)
    
class MessageAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = MessageSendSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Message created", data=serializer.data)