from rest_framework import serializers
from authentication.models import CustomUser
from .models import Resume, Education, Experience, Language
from baseapp.models import Skill
from baseapp.utils import field_error

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['name']

class ResumeSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    class Meta:
        model = Resume
        fields = ['id', 'title', 'region', 'expected_salary', 'about', 'skills', 'is_public']
        read_only_fields = ['id']
        
    def get_skills(self, obj):
        return SkillSerializer(obj.skills.all(), many=True).data
    
    def create(self, validated_data):
        user = self.context.get('user')
        if user.resume:
            return field_error("resume", "User already have resume object, edit it")
        return super().create(validated_data)