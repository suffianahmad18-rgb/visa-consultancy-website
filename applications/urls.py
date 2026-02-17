# applications/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/create/', views.ApplicationCreateView.as_view(), name='application_create'),  # ADD THIS
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='application_update'),
    path('applications/<int:pk>/upload/', views.upload_document, name='upload_document'),
]