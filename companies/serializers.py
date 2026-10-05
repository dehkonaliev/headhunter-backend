from rest_framework import serializers
from baseapp.utils import field_error
from authentication.models import CustomUser
from .models import Company
from vacancies.models import Vacancy


class MiniVacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'salary_from', 'salary_to', 'status']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'description', 'region', 'employees_count']
        read_only_fields = ['id']

class CompanyGetSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    vacancies = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'description', 'region', 'employees_count', 'region',
            'vacancies',
        ] 
        
    def get_region(self, obj):
        return f"{obj.region}, {obj.region.region}"
    
    def get_vacancies(self, obj):
        return MiniVacancySerializer(obj.vacancies.all(), many=True).data