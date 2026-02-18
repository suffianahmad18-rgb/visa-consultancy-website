# testimonials/admin.py
from django.contrib import admin

from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "country",
        "visa_category",
        "rating",
        "is_approved",
        "is_featured",
        "created_at",
    )
    list_filter = (
        "visa_category",
        "country",
        "is_approved",
        "is_featured",
        "created_at",
    )
    search_fields = ("client_name", "testimonial_text", "university", "course")
    list_editable = ("is_approved", "is_featured")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Client Information", {"fields": ("client_name", "client_image", "country")}),
        ("Visa Details", {"fields": ("visa_category", "university", "course")}),
        ("Testimonial", {"fields": ("testimonial_text", "rating")}),
        ("Status", {"fields": ("is_approved", "is_featured")}),
    )
