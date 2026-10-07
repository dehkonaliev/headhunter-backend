from rest_framework import serializers

from vacancies.models import Vacancy
from .models import Company

from baseapp.models import Region


class RegionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']


class CompanyListSerializer(serializers.ModelSerializer):

    region = RegionShortSerializer(read_only=True)
    vacancies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'region', 'employees_count',
                  'is_verified', 'vacancies_count']


class CompanyDetailSerializer(serializers.ModelSerializer):
    region = RegionShortSerializer(read_only=True)
    vacancies_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'description', 'website', 'region',
                  'employees_count', 'is_verified', 'owner', 'vacancies_count',
                  'created_at', 'updated_at']


class CompanyCreateUpdateSerializer(serializers.ModelSerializer):


    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'description', 'website', 'region',
                  'employees_count', 'is_verified', 'owner',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'is_verified', 'owner', 'created_at', 'updated_at']


class CompanyVerifySerializer(serializers.Serializer):
    is_verified = serializers.BooleanField()


class CompanyVacancySerializer(serializers.ModelSerializer):

    region = RegionShortSerializer(read_only=True)

    class Meta:
        model = Vacancy
        fields = ['id', 'title', 'region', 'salary_from', 'salary_to',
                  'currency', 'experience', 'employment_type', 'published_at']