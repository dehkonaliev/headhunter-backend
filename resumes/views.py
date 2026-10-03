from django.shortcuts import render
from .models import Resume, Experience, Education, Language
from authentication.models import CustomUser
from .serializers import ResumeSerializer
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
        serializer = ResumeSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Resume created", data=serializer.data, status_code=201)
    
    def patch(self, request):
        serializer = ResumeSerializer(data=request.data, instance=request.user.resume, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Resume updated", data=serializer.data)
    

class ResumeAPIView(APIView):
    permission_classes = [IsEmployee, IsOwnerOrReadOnly]
    def get(self, request, pk):
        resume = Resume.objects.filter(pk=pk).first()
        if not resume.is_public and request.user != resume.user:
            return error_response(message="Resume not found", status_code=404)
        return success_response(message="Resume details", data=ResumeSerializer(resume).data)