from django.db import models
from companies.models import Company
from baseapp.models import BaseModel, District, Skill, Category

class Vacancy(BaseModel):
    class EmployementTypes(models.TextChoices):
        ON_SITE = "ON_SITE", 'on_site'
        REMOTE = 'REMOTE', 'remote'
        HYBRID = "HYBRID", 'hybrid'
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", 'active'
        DRAFT = "DRAFT", 'draft'
        ARCHIVED = "ARCHIVED", 'archived'
        
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=5000)
    requirements = models.CharField(max_length=2000)
    salary_from = models.PositiveIntegerField()
    salary_to = models.PositiveIntegerField()
    experience = models.CharField(max_length=30)
    employement_type = models.CharField(max_length=50, choices=EmployementTypes.choices)
    skills = models.ManyToManyField(Skill, related_name='required_skills')
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    published_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    


    