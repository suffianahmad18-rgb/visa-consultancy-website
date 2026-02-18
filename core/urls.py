# core/urls.py - Update with new view
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.contact_view, name="contact"),
    path("faq/", views.FAQView.as_view(), name="faq"),
]
