from django.shortcuts import render
from .models import Resume, Experience, Education, Language
from authentication.models import CustomUser
from .serializers import (ResumeSerializer, SkillAddRemoveSerializer, EducationSerializer,
    ExperienceSerializer, LanguageEditSerializer)
from rest_framework.views import APIView
from baseapp.permissions import IsOwnerOrReadOnly, IsEmployee
from baseapp.utils import success_response, error_response


class ResumeCreateAPIView(APIView):
    permission_classes = [IsEmployee]
    def get(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if not resume:
            return error_response(message="Resume not found", status_code=404)
        return success_response(message="Resume details", data=ResumeSerializer(resume).data)
    
    def post(self, request):
        resume = Resume.objects.filter(user=request.user).exists()
        if resume:
            return error_response(message="Resume already exist")
        serializer = ResumeSerializer(data=request.data, context={'resume': resume, 'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Resume created", data=serializer.data, status_code=201)
    
    def patch(self, request):
        serializer = ResumeSerializer(data=request.data, instance=request.user.resume, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Resume updated", data=serializer.data)
    

class ResumeAPIView(APIView):
    permission_classes = [IsEmployee]
    def get(self, request, pk):
        resume = Resume.objects.filter(pk=pk).first()
        if not resume.is_public and request.user != resume.user:
            return error_response(message="Resume not found", status_code=404)
        return success_response(message="Resume details", data=ResumeSerializer(resume).data)
    
class SkillAPIView(APIView):
    permission_classes = [IsEmployee]
    def patch(self, request):
        resume = Resume.objects.filter(user=request.user).first()
        if not resume:
            return error_response(message="Resume not found", status_code=404)
        serializer = SkillAddRemoveSerializer(data=request.data, instance=resume)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Skills added", data=serializer.data)
    
    def delete(self, request):
        resume = Resume.objects.filter(user=request.user).prefetch_related('skills').first()
        if not resume:
            return error_response(message="Resume not found", status_code=404)
        serializer = SkillAddRemoveSerializer(data=request.data, instance=resume)
        serializer.is_valid(raise_exception=True)
        
        resume.skills.remove(*serializer.validated_data.get('skills', []))
        
        return success_response(message="Selected skills removed", data=SkillAddRemoveSerializer(resume).data)
    
class EducationAddAPIView(APIView):
    permission_classes = [IsEmployee]
    def post(self, request):
        serializer = EducationSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Education added", data=serializer.data)  
    
class EducationEditAPIView(APIView):
    permission_classes = [IsEmployee]
    def patch(self, request, pk):
        education = Education.objects.filter(pk=pk, resume=request.user.resume).first()
        if not education:
            return error_response(message="Education not found", status_code=404)
        serializer = EducationSerializer(data=request.data, instance=education, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Education updated", data=serializer.data)
    
    def delete(self, request, pk):
        education = Education.objects.filter(pk=pk, resume=request.user.resume).first()
        if not education:
            return error_response(message="Education not found", status_code=404)
        education.delete()
        
        return success_response(message="Education deteled")
        
class ExperienceAddAPIView(APIView):
    permission_classes = [IsEmployee]
    def post(self, request):
        serializer = ExperienceSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Education added", data=serializer.data)  
    
class ExperienceEditAPIView(APIView):
    permission_classes = [IsEmployee]
    def patch(self, request, pk):
        experience = Experience.objects.filter(pk=pk, resume=request.user.resume).first()
        if not experience:
            return error_response(message="Experience not found", status_code=404)
        serializer = ExperienceSerializer(data=request.data, instance=experience, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Experience updated", data=serializer.data)
    
    def delete(self, request, pk):
        experience = Experience.objects.filter(pk=pk, resume=request.user.resume).first()
        if not experience:
            return error_response(message="Experience not found", status_code=404)
        experience.delete()
        
        return success_response(message="Experience deteled")
    
class LanguageAddAPIView(APIView):
    permission_classes = [IsEmployee]
    def post(self, request):
        if not request.user.resume:
            return error_response(message="Resume not found, create one first!")
        serializer = LanguageEditSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Language added", data=serializer.data)  
    
class LanguageEditAPIView(APIView):
    permission_classes = [IsEmployee]
    def patch(self, request, pk):
        language = Language.objects.filter(pk=pk, resume=request.user.resume).first()
        if not language:
            return error_response(message="Language not found", status_code=404)
        serializer = LanguageEditSerializer(data=request.data, instance=language, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Language updated", data=serializer.data)
    
    def delete(self, request, pk):
        language = Language.objects.filter(pk=pk, resume=request.user.resume).first()
        if not language:
            return error_response(message="Language not found", status_code=404)
        language.delete()
        
        return success_response(message="Language deteled")