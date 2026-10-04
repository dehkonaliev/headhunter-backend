from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class Region(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Skill(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
class Lang(models.Model):
    name = models.CharField(max_length=50, unique=True)
    country_code = models.CharField(max_length=5)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    