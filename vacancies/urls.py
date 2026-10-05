from django.urls import path
from .views import VacancyCreateListAPIVIew, VacancyAPIView, VacancyDetailPrivateGet, VacancyListPrivate


urlpatterns = [
    path('vacancy-list-create', VacancyCreateListAPIVIew.as_view()),
    path('vacancy/<uuid:pk>', VacancyAPIView.as_view()),
    path('my-vacancies', VacancyListPrivate.as_view()),
    path('my-vacancy/<uuid:pk>', VacancyDetailPrivateGet.as_view()),
]