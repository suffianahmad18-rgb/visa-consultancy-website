import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from model_bakery import baker

from study_destinations.models import StudyDestination  # Changed from visas


@pytest.mark.django_db
class TestAuthenticationViews:
    def test_register_view_get(self):
        """Test register page loads"""
        client = Client()
        response = client.get(reverse("accounts:register"))
        assert response.status_code == 200

    def test_register_view_post_success(self):
        """Test successful registration"""
        client = Client()
        data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "first_name": "New",
            "last_name": "User",
            "password1": "ComplexPass123!",
            "password2": "ComplexPass123!",
            "phone": "+1234567890",
            "address": "Test Address",
            "country": "Test Country",
        }

        response = client.post(reverse("accounts:register"), data)
        assert response.status_code == 302
        assert User.objects.filter(username="newuser").exists()

    def test_login_view(self):
        """Test login functionality"""
        user = User.objects.create_user(username="testuser", password="testpass123")

        client = Client()
        response = client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "testpass123"},
        )

        assert response.status_code == 302


@pytest.mark.django_db
class TestApplicationViews:
    def test_application_list_view_requires_login(self):
        """Test application list requires login"""
        client = Client()
        response = client.get(reverse("dashboard:application_list"))
        assert response.status_code == 302
        assert "login" in response.url
