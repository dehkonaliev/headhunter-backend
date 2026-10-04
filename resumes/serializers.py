from rest_framework import serializers
from authentication.models import CustomUser
from .models import Resume, Education, Experience, Language
from baseapp.models import Skill
from baseapp.utils import field_error

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        read_only_fields = ['id']

class LanguageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Language
        fields = ['id', 'name', 'level']
        read_only_fields = ['id']
        
    def get_name(self, obj):
        return obj.name.name
    
class LanguageEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'level']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        resume = Resume.objects.filter(user=self.context.get('user')).first()
        if not resume:
            return field_error("resume", "You do not have a resume, create it first")
        if Language.objects.filter(resume=resume, name=validated_data['name']):
            return field_error("name", "You already have this language in your resume, just edit it")
        validated_data['resume'] = resume
        return super().create(validated_data)
        
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company_name', 'position', 'start_date', 'end_date', 'description']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        resume = Resume.objects.filter(user=self.context.get('user')).first()
        if not resume:
            return field_error("resume", "You do not have a resume, create it first")
        validated_data['resume'] = resume
        return super().create(validated_data)
        
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'speciality', 'degree', 'start_date', 'end_date']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        resume = Resume.objects.filter(user=self.context.get('user')).first()
        if not resume:
            return field_error("resume", "You do not have a resume, create it first")
        validated_data['resume'] = resume
        return super().create(validated_data)

class ResumeSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    class Meta:
        model = Resume
        fields = ['id', 'title', 'region', 'expected_salary', 'about', 'skills', 'is_public', 'experiences', 'educations', 'languages']
        read_only_fields = ['id', 'skills']
        
    def get_skills(self, obj):
        return SkillSerializer(obj.skills.all(), many=True).data
    
    def get_languages(self, obj):
        return LanguageSerializer(obj.langs.all(), many=True).data
    
    def get_educations(self, obj):
        return EducationSerializer(obj.educations.all(), many=True).data
    
    def get_experiences(self, obj):
        return ExperienceSerializer(obj.experiences.all(), many=True).data
    
    def create(self, validated_data):
        resume = self.context.get('resume')
        user = self.context.get('user')
        if resume:
            return field_error("resume", "User already have resume object, edit it")
        validated_data['user'] = user
        return super().create(validated_data)
    
class SkillAddRemoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['skills']

    def update(self, instance, validated_data):
        skills = validated_data.get('skills', [])
        instance.skills.add(*skills)
        return instance

    