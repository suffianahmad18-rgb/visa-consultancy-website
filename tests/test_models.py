import pytest
from django.contrib.auth.models import User
from model_bakery import baker

from applications.models import Application, Document
from study_destinations.models import StudyDestination


@pytest.mark.django_db
class TestApplicationModel:
    def test_application_creation(self, client_user, study_destination):
        """Test application creation"""
        # ✅ Use Django's create() instead of baker.make() for this test
        app = Application.objects.create(
            client=client_user,
            destination=study_destination,
            full_name="Test User",
            phone_number="1234567890",
            email="test@test.com",
            last_qualification="Bachelor",
            grade_marks="85%",
            completion_year=2024,
            destination_country="Test Country",
            preferred_course="CS",
        )
        assert app.application_id.startswith("APP-")
        assert app.client is not None
        assert app.destination is not None

    def test_application_status_progress(self, visa_application):
        """Test progress percentage calculation"""
        status_progress_map = {
            "SUBMITTED": 20,
            "UNDER_REVIEW": 40,
            "DOCS_REQUIRED": 50,
            "PROCESSING": 70,
            "APPROVED": 100,
            "REJECTED": 100,
        }

        for status, expected_progress in status_progress_map.items():
            visa_application.status = status
            visa_application.save()  # Save after changing status
            assert visa_application.progress_percentage == expected_progress


@pytest.mark.django_db
class TestDocumentModel:
    def test_document_creation(self, visa_application):
        """Test document creation"""
        document = baker.make(
            Document,
            application=visa_application,
            document_type="PASSPORT",
            file="test.pdf",
        )

        assert document.application == visa_application
        assert document.document_type == "PASSPORT"
        assert not document.verified

    def test_document_str_representation(self, visa_application):
        """Test string representation"""
        document = baker.make(Document, application=visa_application, document_type="PASSPORT")

        expected_str = f"Passport - {visa_application.application_id}"
        assert str(document) == expected_str
