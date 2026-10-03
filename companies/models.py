from django.db import models
from authentication.models import CustomUser
from baseapp.models import BaseModel, District


class Company(BaseModel):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_role': "EMPLOYER"})
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    region = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    employees_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    