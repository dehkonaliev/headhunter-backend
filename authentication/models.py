from django.db import models
from django.contrib.auth.models import AbstractUser
from baseapp.models import BaseModel
from django.utils import timezone
from datetime import timedelta
import secrets


class CustomUser(AbstractUser, BaseModel):
    class UserRole(models.TextChoices):
        EMPLOYER = 'EMPLOYER', 'employer'
        EMPLOYEE = 'EMPLOYEE', 'employee'
    user_role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.EMPLOYEE)
    summary = models.CharField(max_length=2000, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='avatars/', blank=True, null=True)
    profile_thumbnail = models.ImageField(upload_to='avatars_thumb/', blank=True, null=True)



def default_expiry():
    return timezone.now() + timedelta(minutes=15)

class TempUser(BaseModel):
    email = models.EmailField(max_length=100)
    code = models.IntegerField(blank=True, null=True)
    expiry_time = models.DateTimeField(default=default_expiry)
    
def generate_token():
    return secrets.token_urlsafe(32)
    
class MyToken(BaseModel):
    temp_user = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name='my_tokens')
    token = models.CharField(max_length=64, default=generate_token)