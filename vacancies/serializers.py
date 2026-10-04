from rest_framework import serializers
from authentication.models import CustomUser
from baseapp.utils import field_error
from .models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ['id', 'company', 'title', 'category', 'region', 
            'description', 'requirements', 'salary_from', 'salary_to',
            'experience', 'employement_type', 'skills', 'status',
            'published_at', 'expires_at'
        ]
        read_only_fields = ['id', 'published_at']