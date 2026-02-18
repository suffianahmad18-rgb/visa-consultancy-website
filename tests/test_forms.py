import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.forms import UserRegisterForm
from applications.forms import DocumentUploadForm  # Removed ApplicationForm import


@pytest.mark.django_db
class TestUserRegistrationForm:
    def test_valid_registration_form(self):
        """Test valid registration data"""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
            "phone": "+1234567890",
            "address": "123 Test St",
            "country": "Testland",
        }

        form = UserRegisterForm(data=form_data)
        assert form.is_valid()

    def test_invalid_email(self):
        """Test registration with invalid email"""
        form_data = {
            "username": "testuser",
            "email": "invalid-email",
            "first_name": "Test",
            "last_name": "User",
            "password1": "ComplexPassword123!",
            "password2": "ComplexPassword123!",
            "phone": "+1234567890",
            "address": "123 Test St",
            "country": "Testland",
        }

        form = UserRegisterForm(data=form_data)
        assert not form.is_valid()
        assert "email" in form.errors

    def test_password_mismatch(self):
        """Test password confirmation mismatch"""
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "Password123!",
            "password2": "DifferentPassword123!",
            "phone": "+1234567890",
            "address": "123 Test St",
            "country": "Testland",
        }

        form = UserRegisterForm(data=form_data)
        assert not form.is_valid()
        assert "password2" in form.errors


class TestDocumentUploadForm:
    def test_valid_document_upload(self):
        """Test valid document upload"""
        file_content = b"Test PDF content"
        uploaded_file = SimpleUploadedFile("test.pdf", file_content, content_type="application/pdf")

        form_data = {"document_type": "PASSPORT"}

        form = DocumentUploadForm(data=form_data, files={"file": uploaded_file})
        assert form.is_valid()
