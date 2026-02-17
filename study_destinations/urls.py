# study_destinations/urls.py
from django.urls import path
from . import views

app_name = 'study_destinations'

urlpatterns = [
    path('', views.StudyDestinationListView.as_view(), name='list'),
    path('<slug:slug>/', views.StudyDestinationDetailView.as_view(), name='detail'),
]