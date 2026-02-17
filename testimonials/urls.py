# testimonials/urls.py
from django.urls import path
from . import views

app_name = 'testimonials'

urlpatterns = [
    path('', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('study-visa/', views.StudyVisaTestimonialsView.as_view(), name='study_visa_testimonials'),
]