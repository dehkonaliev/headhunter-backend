from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company
from .serializers import (
    CompanyListSerializer,
    CompanyDetailSerializer,
    CompanyCreateUpdateSerializer,
    CompanyVerifySerializer,
    CompanyVacancySerializer,
)


class CompanyPagination(PageNumberPagination):
    page_size = 20


def companies_queryset():
    return (
        Company.objects
        .select_related('region', 'owner')
        .annotate(vacancies_count=Count('vacancies'))
        .order_by('-created_at')
    )


def check_employer(user):
    if getattr(user, 'user_role', None) != 'EMPLOYER':
        raise PermissionDenied()



class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = companies_queryset()
    pagination_class = CompanyPagination
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['region', 'employees_count', 'is_verified']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompanyCreateUpdateSerializer
        return CompanyListSerializer

    def perform_create(self, serializer):
        check_employer(self.request.user)
        serializer.save(owner=self.request.user)



class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = companies_queryset()
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ['get', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CompanyDetailSerializer
        return CompanyCreateUpdateSerializer

    def get_object(self):
        company = super().get_object()
        if self.request.method in ('PATCH', 'DELETE') and company.owner != self.request.user:
            raise PermissionDenied()
        return company


class MyCompaniesView(generics.ListAPIView):
    serializer_class = CompanyListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CompanyPagination

    def get_queryset(self):
        check_employer(self.request.user)
        return companies_queryset().filter(owner=self.request.user)


class CompanyVacanciesView(generics.ListAPIView):
    serializer_class = CompanyVacancySerializer
    permission_classes = [AllowAny]
    pagination_class = CompanyPagination

    def get_queryset(self):
        company = get_object_or_404(Company, pk=self.kwargs['pk'])
        vacancies = company.vacancies.select_related('region')

        user = self.request.user
        is_owner = user.is_authenticated and company.owner_id == user.id
        if not is_owner:
            vacancies = vacancies.filter(status='active').filter(
                Q(expires_at__isnull=True) | Q(expires_at__gte=timezone.now())
            )
        return vacancies.order_by('-published_at')


class CompanyVerifyView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        company = get_object_or_404(Company, pk=pk)

        serializer = CompanyVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company.is_verified = serializer.validated_data['is_verified']
        company.save(update_fields=['is_verified'])

        return Response(
            {'id': company.id, 'name': company.name, 'is_verified': company.is_verified},
            status=status.HTTP_200_OK,
        )