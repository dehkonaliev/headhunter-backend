from django.urls import path

from .views import ApplicationCreateView, ApplicationListView, ApplicationDetailView, ApplicationStatusView, VacancyApplicationsView



urlpatterns = [
    path("vacancies/<int:id>/apply/", ApplicationCreateView.as_view(), name="application-create"),
    path("applications/", ApplicationListView.as_view(), name="application-list"),
    path("applications/<int:pk>/", ApplicationDetailView.as_view(), name="application-detail"),
    path("applications/<int:pk>/status/", ApplicationStatusView.as_view(), name="application-status"),
    path("vacancies/<int:id>/applications/", VacancyApplicationsView.as_view(), name="vacancy-applications"),
]