from rest_framework import serializers
from .models import Chat, Message
from authentication.models import CustomUser
from baseapp.utils import field_error

class MessageMiniSerializer(serializers.ModelSerializer):
    context = serializers.SerializerMethodField()
    class Meta:
        model = Message
        fields = ['context', 'message_type']
        
    def get_context(self, obj):
        return obj.context[:30] + "..."

class ChatMiniEmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = Chat
        fields = ['id', 'company_name', 'last_message']
    
    def get_company_name(self, obj):
        return obj.company.name
    
    def get_last_message(self, obj):
        last_message = obj.messages.all().order_by('-created_at').first()
        return MessageMiniSerializer(last_message).data
    

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'user', 'company', 'status']
        read_only_fields = ['id', 'status']
        
    def validate_employee(self, user):
        if not user.resume:
            return field_error("user", "You do not have a resume, please create one first")
        
        return user
    
    def validate_company(self, company):
        if not company.is_verified:
            return field_error("company", "Company is not verified")
        
        return company
    
    def validate(self, attrs):
        company = attrs['company']
        employee = attrs['user']
        
        if Chat.objects.filter(user=employee, company=company).exists():
            return field_error("non_field_error", "This chat already exists")
        

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'message_type', 'context', 'application', 'sender']
        read_only_fields = ['id', 'message_type', 'application', 'sender']

class MessageSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'message_type', 'context', 'sender']
        read_only_fields = ['id', 'chat', 'message_type', 'sender']
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        
    def create(self, validated_data):
        sender = self.context.get('user')
        chat = self.context.get('chat')
        
        if sender.user_role == CustomUser.UserRole.EMPLOYEE and chat.user != sender:
            return field_error("chat", "Chat not found")
        elif sender.user_role == CustomUser.UserRole.EMPLOYER and chat.company.user != sender:
            return field_error('chat', "Chat not found")
        elif sender.user_role not in CustomUser.UserRole.choices:
            return field_error("user", "User not found")     
        validated_data['message_type'] = Message.MessageTypes.MESSAGE
        return super().create(validated_data)
        
        