# appointments/models.py
from django.contrib.auth.models import User
from django.db import models


class Appointment(models.Model):
    APPOINTMENT_TYPES = [
        ("CONSULTATION", "Consultation"),
        ("DOCUMENT_SUBMISSION", "Document Submission"),
        ("FOLLOW_UP", "Follow-up"),
        ("INTERVIEW_PREP", "Interview Preparation"),
    ]

    APPOINTMENT_STATUS = [
        ("SCHEDULED", "Scheduled"),
        ("CONFIRMED", "Confirmed"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
        ("NO_SHOW", "No Show"),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client_appointments")
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="staff_appointments",
        limit_choices_to={"is_staff": True},
    )
    appointment_type = models.CharField(max_length=50, choices=APPOINTMENT_TYPES)
    scheduled_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default="SCHEDULED")
    purpose = models.TextField()
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment: {self.client.get_full_name()} with {self.staff.get_full_name()} - {self.scheduled_date}"
