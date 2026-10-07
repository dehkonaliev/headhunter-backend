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
        fields = ['id', 'employee', 'company', 'status']
        read_only_fields = ['id', 'status']
        
    def validate_employee(self, employee):
        if not employee.resume:
            return field_error("employee", "You do not have a resume, please create one first")
        
        return employee
    
    def validate_company(self, company):
        if not company.is_verified:
            return field_error("company", "Company is not verified")
        
        return company
    
    def validate(self, attrs):
        company = attrs['company']
        employee = attrs['employee']
        
        if Chat.objects.filter(employee=employee, company=company).exists():
            return field_error("non_field_error", "This chat already exists")
        

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'message_type', 'context', 'application']
        read_only_fields = ['id', 'message_type', 'application']
    
    def create(self, validated_data):
        validated_data['message_type'] = Message.MessageTypes.MESSAGE
        return super().create(validated_data)