from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .permissions import IsEmployee, IsEmployer, IsVacancyOwner
from .serializers import ApplicationCreateSerializer, ApplicationListSerializer, ApplicationDetailSerializer, ApplicationStatusSerializer
from vacancies.models import Vacancy


class ApplicationPagination(PageNumberPagination):
    page_size = 20


class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    permission_classes = [IsAuthenticated, IsEmployee]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["vacancy"] = get_object_or_404(Vacancy, pk=self.kwargs["id"])
        return context


class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ApplicationPagination

    def get_queryset(self):
        user = self.request.user

        if user.user_role == "EMPLOYEE":
            queryset = Application.objects.filter(resume__employee=user)
        elif user.user_role == "EMPLOYER":
            queryset = Application.objects.filter( vacancy__company__owner=user)
        else:
            queryset = Application.objects.none()
        queryset = queryset.select_related("vacancy__company", "resume__employee",)

        status = self.request.query_params.get("status")
        vacancy = self.request.query_params.get("vacancy")
        resume = self.request.query_params.get("resume")
        ordering = self.request.query_params.get("ordering")

        if status:
            queryset = queryset.filter(status=status)
        if vacancy:
            queryset = queryset.filter(vacancy_id=vacancy)
        if resume:
            queryset = queryset.filter(resume_id=resume)
        if ordering in ["created_at", "-created_at"]:
            queryset = queryset.order_by(ordering)
        return queryset


class ApplicationDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsEmployee()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        queryset = Application.objects.select_related("vacancy__company", "resume__employee").prefetch_related("resume__skills", "resume__employee__educations", "resume__employee__experiences", "resume__employee__langs",)

        if user.user_role == "EMPLOYEE":
            return queryset.filter(resume__employee=user)

        if user.user_role == "EMPLOYER":
            return queryset.filter(vacancy__company__owner=user)

        return queryset.none()

    def get_serializer_class(self):
        return ApplicationDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        application = self.get_object()

        if request.user.user_role == "EMPLOYER" and application.status == Application.Status.NEW:
            application.status = Application.Status.VIEWED
            application.save()

        serializer = self.get_serializer(application)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        application = self.get_object()

        if application.status == Application.Status.INTERVIEW:
            return Response({"detail": ("Suhbatga taklif qilingan murojaatni qaytarib olib bo'lmaydi.")},status=400)

        application.delete()

        return Response(status=204)


class ApplicationStatusView(generics.UpdateAPIView):
    serializer_class = ApplicationStatusSerializer

    permission_classes = [IsAuthenticated, IsEmployer, IsVacancyOwner]

    def get_queryset(self):
        return Application.objects.select_related("vacancy__company")

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        serializer = self.get_serializer(application, data=request.data, partial=True,)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
                "id": application.id,
                "status": application.status,
                "updated_at": application.updated_at,
            })


class VacancyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationListSerializer

    permission_classes = [IsAuthenticated, IsEmployer, IsVacancyOwner]

    pagination_class = ApplicationPagination

    def get_queryset(self):
        vacancy = get_object_or_404( Vacancy, pk=self.kwargs["id"])

        self.check_object_permissions(self.request,vacancy)

        queryset = Application.objects.filter(vacancy=vacancy).select_related("vacancy__company","resume__employee",)
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        return queryset