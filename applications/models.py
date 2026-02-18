from django.contrib.auth.models import User
from django.db import models

from study_destinations.models import StudyDestination


class Application(models.Model):
    STATUS_CHOICES = [
        ("SUBMITTED", "Submitted"),
        ("UNDER_REVIEW", "Under Review"),
        ("DOCS_REQUIRED", "Additional Documents Required"),
        ("PROCESSING", "Processing"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    ENGLISH_TEST_CHOICES = [
        ("IELTS", "IELTS"),
        ("TOEFL", "TOEFL"),
        ("PTE", "PTE Academic"),
        ("DUOLINGO", "Duolingo English Test"),
        ("CAMBRIDGE", "Cambridge English"),
        ("NONE", "No English Test Taken"),
        ("OTHER", "Other"),
    ]

    application_id = models.CharField(max_length=20, unique=True, editable=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    destination = models.ForeignKey(
        "study_destinations.StudyDestination",
        on_delete=models.PROTECT,
        related_name="applications",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="SUBMITTED")

    # Personal Information
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    # Education Details
    last_qualification = models.CharField(max_length=200, help_text="e.g., Bachelor's in Computer Science")
    grade_marks = models.CharField(max_length=100, help_text="e.g., 85%, GPA 3.5/4.0")
    completion_year = models.IntegerField(help_text="Year of completion")

    # Destination & Course
    destination_country = models.CharField(max_length=100)
    preferred_course = models.CharField(max_length=200, help_text="e.g., MS in Computer Science")

    # English Test
    english_test = models.CharField(max_length=50, choices=ENGLISH_TEST_CHOICES, default="NONE")
    english_score = models.CharField(max_length=100, blank=True, help_text="e.g., IELTS 6.5 bands, TOEFL 90")

    # Visa History
    visa_refusal = models.BooleanField(default=False, help_text="Any previous visa refusal?")
    visa_refusal_details = models.TextField(blank=True, help_text="If yes, provide details")

    # Staff assignment
    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_applications",
    )

    # Timestamps
    submitted_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    decision_date = models.DateField(null=True, blank=True)

    # Additional fields
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.application_id:
            import random
            from datetime import datetime

            prefix = "APP"
            year_month = datetime.now().strftime("%Y%m")
            random_num = random.randint(1000, 9999)
            self.application_id = f"{prefix}-{year_month}-{random_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_id} - {self.full_name or self.client.get_full_name()}"

    class Meta:
        ordering = ["-submitted_date"]

    @property
    def progress_percentage(self):
        status_progress = {
            "SUBMITTED": 20,
            "UNDER_REVIEW": 40,
            "DOCS_REQUIRED": 50,
            "PROCESSING": 70,
            "APPROVED": 100,
            "REJECTED": 100,
        }
        return status_progress.get(self.status, 0)


class Document(models.Model):
    DOCUMENT_TYPES = [
        ("PASSPORT", "Passport"),
        ("PHOTO", "Photograph"),
        ("BANK_STATEMENT", "Bank Statement"),
        ("EMPLOYMENT_LETTER", "Employment Letter"),
        ("INVITATION_LETTER", "Invitation Letter"),
        ("EDUCATION_CERTIFICATE", "Education Certificate"),
        ("TRANSCRIPT", "Academic Transcript"),
        ("ENGLISH_TEST", "English Test Result"),
        ("POLICE_CLEARANCE", "Police Clearance"),
        ("MEDICAL_REPORT", "Medical Report"),
        ("OTHER", "Other"),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to="application_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.application.application_id}"
