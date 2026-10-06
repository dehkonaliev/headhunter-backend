from .models import Chat, Message
from authentication.models import CustomUser
from .serializers import ChatSerializer, MessageSerializer
from baseapp.utils import success_response, error_response
from baseapp.permissions import IsEmployee, IsEmployer, IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class ChatEditAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        chat = Chat.objects.filter(pk=pk).first()
        pass
        