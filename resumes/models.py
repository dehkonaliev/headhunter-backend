from django.db import models
from authentication.models import CustomUser
from baseapp.models import BaseModel, District, Skill, Lang

class Resume(BaseModel):
    employee = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='resume', limit_choices_to={'user_role': "EMPLOYEE"})
    title = models.CharField(max_length=50)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    expected_salary = models.PositiveIntegerField(null=True, blank=True)
    about = models.CharField(max_length=5000, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name="user_skills")
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    
class Education(BaseModel):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='educations', limit_choices_to={"user_role": "EMPLOYEE"})
    institution = models.CharField()
    speciality = models.CharField(max_length=50)
    degree = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.employee.first_name} - {self.institution}"
    
class Experience(BaseModel):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='experiences', limit_choices_to={"user_role": "EMPLOYEE"})
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=2000)

class Language(BaseModel):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='langs', limit_choices_to={"user_role": "EMPLOYEE"})
    class Levels(models.TextChoices):
        BEGINNER = "BEGINNER", "beginner"
        INTERMEDIATE = "INTERMEDIATE", 'intermediate'
        ELEMENTARY = 'ELEMENTARY', 'elementary'
        ADVANCED = "ADVANCED", "advanced"
        PROFICIENT = "PROFICIENT", 'proficient'
    name = models.ForeignKey(Lang, on_delete=models.PROTECT)
    level = models.CharField(max_length=15, choices=Levels.choices)
    
    
    
    
    