from django.urls import path
from .views import VacancyCreateListAPIVIew, VacancyAPIView


urlpatterns = [
    path('vacancy-list-create', VacancyCreateListAPIVIew.as_view()),
    path('vacancy/<uuid:pk>', VacancyAPIView.as_view()),
]