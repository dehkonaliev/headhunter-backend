from django.urls import path
from .views import VacancyCreateListAPIVIew


urlpatterns = [
    path('vacancy-list-create', VacancyCreateListAPIVIew.as_view())
]