from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

class Region(BaseModel):
    region = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.region
    
class District(BaseModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.district
    