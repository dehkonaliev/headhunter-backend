
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CreateTempUserAPIView, CreateAccountAPIView, VerifyCodeAPIView,
    LoginAPIView, LogoutAPIView,
)

urlpatterns = [
    path('signup', CreateTempUserAPIView.as_view()),
    path('verify-code', VerifyCodeAPIView.as_view()),
    path('create-account', CreateAccountAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]