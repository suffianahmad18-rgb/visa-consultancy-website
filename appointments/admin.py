# appointments/admin.py
from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "staff",
        "appointment_type",
        "scheduled_date",
        "status",
        "duration_minutes",
    )
    list_filter = ("status", "appointment_type", "scheduled_date")
    search_fields = ("client__username", "staff__username", "purpose")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "scheduled_date"
