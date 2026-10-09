from django.utils import timezone
from rest_framework import serializers

from .models import Application
from resumes.models import Resume


class ApplicationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ["id", "resume", "cover_letter",]
        read_only_fields = ["id",]

    def validate_resume(self, resume):

        user = self.context["request"].user
        if resume.employee != user:
            raise serializers.ValidationError("Bu rezyume sizga tegishli emas.")
        return resume

    def validate(self, attrs):

        vacancy = self.context["vacancy"]

       
        if vacancy.status != "ACTIVE":
            raise serializers.ValidationError("Bu vakansiya faol emas.")

       
        if (vacancy.expires_at and vacancy.expires_at < timezone.now()):
            raise serializers.ValidationError("Bu vakansiyaning muddati tugagan.")

       
        exists = Application.objects.filter(vacancy=vacancy,resume=attrs["resume"]).exists()

        if exists:
            raise serializers.ValidationError("Siz bu vakansiyaga allaqachon murojaat qilgansiz.")

        return attrs

    def create(self, validated_data):

        vacancy = self.context["vacancy"]

        return Application.objects.create(vacancy=vacancy,**validated_data)


class ApplicationListSerializer(serializers.ModelSerializer):

    vacancy_data = serializers.SerializerMethodField()
    resume_data = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Application

        fields = ["id", "vacancy_data", "resume_data", "user_data", "cover_letter", "status", "created_at",]

    def get_vacancy_data(self, obj):

        vacancy = obj.vacancy

        return {"id": vacancy.id, "title": vacancy.title,}

    def get_resume_data(self, obj):

        resume = obj.resume

        return {"id": resume.id, "title": resume.title, "expected_salary": resume.expected_salary, "about": resume.about, "is_public": resume.is_public,}

    def get_user_data(self, obj):

        employee = obj.resume.employee

        return {"id": employee.id, "first_name": employee.first_name, "last_name": employee.last_name,}


class ApplicationDetailSerializer(serializers.ModelSerializer):

    vacancy_data = serializers.SerializerMethodField()
    resume_data = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Application

        fields = ["id", "vacancy_data", "resume_data", "user_data", "cover_letter", "status", "created_at", "updated_at",]

    def get_vacancy_data(self, obj):

        vacancy = obj.vacancy

        return {
            "id": vacancy.id,
            "title": vacancy.title,
            "description": vacancy.description,
            "requirements": vacancy.requirements,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "experience": vacancy.experience,
            "employement_type": vacancy.employement_type,
            "status": vacancy.status,
            "company": {
                "id": vacancy.company.id,
                "name": vacancy.company.name,
            },
        }

    def get_resume_data(self, obj):

        resume = obj.resume

        return {
            "id": resume.id,
            "title": resume.title,
            "region": str(resume.region) if resume.region else None,
            "expected_salary": resume.expected_salary,
            "about": resume.about,
            "skills": [
                str(skill)
                for skill in resume.skills.all()
            ],
            "is_public": resume.is_public,

            "educations": [
                {
                    "institution": education.institution,
                    "speciality": education.speciality,
                    "degree": education.degree,
                    "start_date": education.start_date,
                    "end_date": education.end_date,
                }
                for education in resume.employee.educations.all()
            ],

            "experiences": [
                {
                    "company_name": experience.company_name,
                    "position": experience.position,
                    "start_date": experience.start_date,
                    "end_date": experience.end_date,
                    "description": experience.description,
                }
                for experience in resume.employee.experiences.all()
            ],

            "languages": [
                {
                    "name": str(language.name),
                    "level": language.level,
                }
                for language in resume.employee.langs.all()
            ],
        }

    def get_user_data(self, obj):

        employee = obj.resume.employee

        return {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
        }


class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application

        fields = [
            "status",
        ]

    def validate_status(self, value):

        application = self.instance

        if not application.can_change_to(value):
            raise serializers.ValidationError(f"{application.status} holatidan " f"{value} holatiga o'tib bo'lmaydi.")
        return value