from django.shortcuts import render
from authentication.models import CustomUser
from baseapp.permissions import IsOwnerOrReadOnly, IsEmployer
from .models import Vacancy
from rest_framework.views import APIView
from baseapp.utils import success_response, error_response
from .serializers import VacancySerializer


class VacancyCreateListAPIVIew(APIView):
    permission_classes = [IsEmployer]
    def post(self, request):
        serializer = VacancySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Vacancy created", data=serializer.data)
    
    def get(self, request):
        vacancies = Vacancy.objects.filter(status=Vacancy.StatusChoices.ACTIVE).order_by('-published_at')
        return success_response(message="Vacany suggestions", data=VacancySerializer(vacancies, many=True).data)

class VacancyAPIView(APIView):
    pass