from rest_framework import serializers
from .models import CustomUser, TempUser, MyToken
from baseapp.utils import name_validator, username_validator, password_validator, field_error, code_generate
from django.contrib.auth import authenticate
from django.utils import timezone
from django.db.models import F



class TempUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempUser
        fields = ['id', 'email']
        read_only_fields = ['id']
        
    def create(self, validated_data):
        email = validated_data['email']
        if CustomUser.objects.filter(email=email).exists():
            return field_error("email", "A user with this email already exists")
        temp_user = TempUser.objects.filter(email=email).first()
        if temp_user and temp_user.expiry_time <= timezone.now():
            temp_user.delete()
            temp_user = TempUser.objects.create(email=email, code=code_generate(email))
            return temp_user
        elif temp_user and temp_user.expiry_time > timezone.now():
            return temp_user

        temp_user = TempUser.objects.create(email=email, code=code_generate(email))
        return temp_user
        

class VerifyCodeSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=32, required=False)
    class Meta:
        model = TempUser
        fields = ['id', 'email', 'code', 'token']
        read_only_fields = ['id', 'token']
        
    def validate_email(self, email):
        email = email.strip()
        temp_user = TempUser.objects.filter(email=email).first()
        if not temp_user:
            return field_error("email", "A user with that email not found")
        if temp_user and temp_user.expiry_time <= timezone.now():
            return field_error("email", "Code expired")
        
        return email
    
    def validate(self, attrs):
        code = attrs.get('code')
        if not code:
            return field_error("code", "Code required")
        email = attrs['email']
        
        temp_user = TempUser.objects.filter(email=email).first()
        if temp_user.code != code:
            return field_error("code", "Invalid code")
        
        attrs['temp_user'] = temp_user
        
        return attrs
    
    def create(self, validated_data):
        temp_user = validated_data['temp_user']
        token = MyToken.objects.create(temp_user=temp_user)
        validated_data['token'] = token.token
        
        return validated_data
    
    
class CreateAccountSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)
    conf_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'token', 'username', 'first_name', 'last_name', 'user_role', 'conf_password', 'password']
        read_only_fields = ['id']
        
    def validate_token(self, token):
        token_obj = MyToken.objects.filter(token=token).first()
        if not token_obj:
            return field_error("token", "Token not found")
        return token_obj
    
    def validate_username(self, username):
        return username_validator(username)
    
    def validate_first_name(self, first_name):
        return name_validator(first_name, "first_name")
    
    def validate_last_name(self, last_name):
        return name_validator(last_name, "last_name")
    
    def validate(self, attrs):
        password = attrs['password']
        conf_password = attrs['conf_password']
        
        password_validator(password)
        
        if password != conf_password:
            return field_error("conf_password", "Confirmation password must identical")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('conf_password')
        token_email = validated_data['token'].temp_user.email
        TempUser.objects.filter(email=token_email).delete()
        validated_data.pop('token', None)
        
        validated_data['email'] = token_email
        
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return field_error("credentials", "Invalid username or password.")
        if not user.is_active:
            return field_error("credentials", "User account is disabled.")
        attrs['user'] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        from rest_framework_simplejwt.tokens import RefreshToken
        try:
            token = RefreshToken(value)
            token.blacklist()
        except Exception:
            return field_error("refresh", "Token is invalid or already blacklisted.")
        return value
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'user_role', 'email', 'phone_number', 'profile_photo', 'profile_thumbnail']
        read_only_fields = ['id', 'email', 'user_role']
    
    def validate_username(self, username):
        return username_validator(username)
    
    def validate_first_name(self, first_name):
        return name_validator(first_name, "first_name")
    
    def validate_last_name(self, last_name):
        return name_validator(last_name, "last_name")
