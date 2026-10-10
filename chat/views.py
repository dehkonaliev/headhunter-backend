from .models import Chat, Message
from authentication.models import CustomUser
from .serializers import ChatSerializer, MessageSerializer, ChatMiniEmployeeSerializer, MessageSendSerializer
from baseapp.utils import success_response, error_response
from baseapp.permissions import IsEmployeeStrict, IsEmployer, IsOwnerOrReadOnly, IsOwnerStrict
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class ChatListAPIView(APIView):
    permission_classes = [IsEmployeeStrict]
    def get(self, request):
        chats = Chat.objects.filter(user=request.user)
        
        return success_response(message="Chats list", data=ChatMiniEmployeeSerializer(chats, many=True).data)
    
class MessageCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        chat = Chat.objects.filter(pk=pk).first()
        serializer = MessageSendSerializer(data=request.data, context={'user': request.user, 'chat': chat})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Message created", data=serializer.data)
    
class ChatMessages(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        chat = Chat.objects.filter(Q(user = request.user) | Q(company__user=request.user), pk=pk).prefetch_related('messages').first()
        if not chat:
            return error_response(message="Chat not found")
        messages = chat.messages.order_by('-created_at')
        
        return success_response(message="Chat messages", data=MessageSerializer(messages, many=True).data)
    
class MessageEditAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerStrict]
    def patch(self, request, pk):
        user = request.user
        if user.user_role == CustomUser.UserRole.EMPLOYER:
            message = Message.objects.filter(pk=pk, sender='COMPANY').select_related('chat').select_related('chat__company').first()
            if not message:
                return error_response(message="Message not found at Employer")
            self.check_object_permissions(request, message.chat.company)
        elif user.user_role == CustomUser.UserRole.EMPLOYEE:
            message = Message.objects.filter(pk=pk, sender=CustomUser.UserRole.EMPLOYEE).select_related('chat').first()
            if not message:
                return error_response(message="Message not found")
            self.check_object_permissions(request, message.chat)
        else:
            return error_response(message="User role not found")
        serializer = MessageSendSerializer(data=request.data, context={'user': request.user}, instance=message, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Message edited", data=serializer.data)
    
    def delete(self, request, pk):
        user = request.user
        
        if user.user_role == CustomUser.UserRole.EMPLOYER:
            message = Message.objects.filter(pk=pk, sender='COMPANY').select_related('chat').select_related('chat__company').first()
            if not message:
                return error_response(message="Message not found at Employer")
            self.check_object_permissions(request, message.chat.company)
        elif user.user_role == CustomUser.UserRole.EMPLOYEE:
            message = Message.objects.filter(pk=pk, sender=CustomUser.UserRole.EMPLOYEE).select_related('chat').first()
            if not message:
                return error_response(message="Message not found")
            self.check_object_permissions(request, message.chat)
        else:
            return error_response(message="User role not found")
        
        message.delete()
        return success_response(message="Message deleted")
        
        
        
            
        