# tests/conftest.py
import os
import django
from model_bakery import baker
from model_bakery.random_gen import gen_text

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visa_consultancy.settings')
django.setup()

import pytest
from django.contrib.auth.models import User
from study_destinations.models import StudyDestination
from applications.models import Application

# Add generator for RichTextField
baker.generators.add('ckeditor.fields.RichTextField', gen_text)

@pytest.fixture
def client_user():
    return User.objects.create_user(
        username='client1',
        email='client@test.com',
        password='testpass123',
        first_name='John',
        last_name='Doe'
    )

@pytest.fixture
def study_destination():
    return baker.make(
        StudyDestination,
        country_name='Test Country',
        slug='test-country',
        intro_description='Test description',  # Add this
        is_published=True
    )

@pytest.fixture
def visa_application(client_user, study_destination):
    return baker.make(
        Application,
        client=client_user,
        destination=study_destination,
        full_name="John Doe",
        phone_number="1234567890",
        email="john@test.com",
        last_qualification="Bachelor",
        grade_marks="85%",
        completion_year=2024,
        destination_country="Test Country",
        preferred_course="CS",
        status='SUBMITTED'
    )