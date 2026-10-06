from django.db import models
from authentication.models import CustomUser
from applications.models import Application
from baseapp.models import BaseModel
from companies.models import Company
from applications.models import Application


class Chat(BaseModel):
    class ChatStatus(models.TextChoices):
        ACTIVE = "ACTIVE", 'active'
        BLOCKED = "BLOCKED", 'blocked'
    employee = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='my_chats', 
        limit_choices_to={'user_role': 'EMPLOYEE'}
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='applicants'
    )
    status = models.CharField(max_length=30, choices=ChatStatus.choices, default=ChatStatus.ACTIVE)
    
    class Meta:
        unique_together = ['company', 'employee']
    


class Message(BaseModel):
    class MessageTypes(models.TextChoices):
        APPLICATION = "APPLICATION", 'application'
        DISCARD = "DISCARD", 'discard'
        INTERVIEW = "INTERVIEW", 'interview'
        ARCHIVE = "ARCHIVE", 'archive'
        MESSAGE = "MESSAGE", 'message'
    
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=30, choices=MessageTypes.choices)
    context = models.CharField(max_length=10000)
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    

        