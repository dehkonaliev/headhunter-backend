from .views import (ResumeAPIView, ResumeCreateAPIView, SkillAPIView,
    EducationAddAPIView, EducationEditAPIView, ExperienceAddAPIView,
    ExperienceEditAPIView, LanguageAddAPIView, LanguageEditAPIView)
from django.urls import path

urlpatterns = [
    path('resume', ResumeCreateAPIView.as_view()),
    path('resume-get/<uuid:pk>', ResumeAPIView.as_view()),
    path('skills', SkillAPIView.as_view()),
    path('education-add', EducationAddAPIView.as_view()),
    path('education/<uuid:pk>', EducationEditAPIView.as_view()),
    path('experience-add', ExperienceAddAPIView.as_view()),
    path('experience/<uuid:pk>', ExperienceEditAPIView.as_view()),
    path('language-add', LanguageAddAPIView.as_view()),
    path('language/<uuid:pk>', LanguageEditAPIView.as_view()),
]