from .views import ResumeAPIView, ResumeCreateAPIView, SkillAPIView
from django.urls import path

urlpatterns = [
    path('resume', ResumeCreateAPIView.as_view()),
    path('resume-get/<uuid:pk>', ResumeAPIView.as_view()),
    path('skills', SkillAPIView.as_view()),
]