from .models import (
    CustomUser
)
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q, F
from baseapp.utils import success_response, error_response
from .serializers import (
    TempUserSerializer, CreateAccountSerializer, VerifyCodeSerializer,
    LoginSerializer, LogoutSerializer, ProfileSerializer
)


class CreateTempUserAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = TempUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Temp user created", data=serializer.data, status_code=201)
    

class VerifyCodeAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Code verified", data=serializer.data, status_code=201)
    

class CreateAccountAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Account created", data=serializer.data, status_code=201)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return success_response(
            message="Login successful",
            data={
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            },
            status_code=200,
        )

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(message="Logged out successfully", status_code=200)
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return success_response(message="Profile detail", data=ProfileSerializer(request.user).data)
    
    def patch(self, request):
        serializer = ProfileSerializer(data=request.data, instance=request.user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return success_response(message="Profile updated", data=serializer.data)

class GetUser(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return success_response(message="Anonymous user", data={'user_role': "anonymous"})
        elif user.user_role == CustomUser.UserRole.EMPLOYEE:
            return success_response(message="Employee", data={'user_role': "employee"})
        elif user.user_role == CustomUser.UserRole.EMPLOYER:
            return success_response(message="Employer", data={'user_role': "employer"})
        else:
            return error_response(message="Unexpected error happened")
            