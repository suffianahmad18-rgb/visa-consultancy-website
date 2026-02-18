# study_destinations/admin.py
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    DestinationSection,
    IntakeTable,
    PostStudyWork,
    Scholarship,
    StudyDestination,
    TuitionTable,
    VisaRequirement,
)


class DestinationSectionInline(admin.TabularInline):
    model = DestinationSection
    extra = 1
    fields = ["section_title", "section_type", "order", "is_active"]
    ordering = ["order"]


class TuitionTableInline(admin.TabularInline):
    model = TuitionTable
    extra = 1
    fields = [
        "program_name",
        "program_level",
        "tuition_fee_min",
        "tuition_fee_max",
        "duration_years",
        "order",
    ]


class IntakeTableInline(admin.TabularInline):
    model = IntakeTable
    extra = 1
    fields = [
        "intake_name",
        "intake_month",
        "application_deadline",
        "is_main_intake",
        "order",
    ]


class ScholarshipInline(admin.TabularInline):
    model = Scholarship
    extra = 1
    fields = ["scholarship_title", "scholarship_type", "amount", "is_active", "order"]


class VisaRequirementInline(admin.TabularInline):
    model = VisaRequirement
    extra = 1
    fields = ["visa_name", "visa_type", "processing_time", "visa_fee", "order"]


class PostStudyWorkInline(admin.TabularInline):
    model = PostStudyWork
    extra = 1
    fields = ["visa_name", "duration", "order"]


@admin.register(StudyDestination)
class StudyDestinationAdmin(admin.ModelAdmin):
    list_display = [
        "country_name",
        "country_code",
        "is_published",
        "is_featured",
        "order",
        "created_at",
    ]
    list_filter = ["country_code", "is_published", "is_featured", "created_at"]
    search_fields = ["country_name", "intro_title", "intro_description"]
    prepopulated_fields = {"slug": ("country_name",)}
    list_editable = ["is_published", "is_featured", "order"]
    readonly_fields = ["created_at", "updated_at", "preview_link"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("country_name", "country_code", "slug", "banner_image")},
        ),
        ("Introduction", {"fields": ("intro_title", "intro_description")}),
        (
            "Quick Facts",
            {
                "fields": (
                    "quick_fact_1",
                    "quick_fact_2",
                    "quick_fact_3",
                    "quick_fact_4",
                )
            },
        ),
        (
            "SEO & Settings",
            {
                "fields": (
                    "meta_title",
                    "meta_description",
                    "is_published",
                    "is_featured",
                    "order",
                )
            },
        ),
        ("Preview", {"fields": ("preview_link",), "classes": ("collapse",)}),
    )

    inlines = [
        DestinationSectionInline,
        TuitionTableInline,
        IntakeTableInline,
        ScholarshipInline,
        VisaRequirementInline,
        PostStudyWorkInline,
    ]

    def preview_link(self, obj):
        if obj.pk:
            return format_html(
                '<a href="{}" target="_blank">View Live Page</a>',
                obj.get_absolute_url(),
            )
        return "Save first to preview"

    preview_link.short_description = "Page Preview"


@admin.register(DestinationSection)
class DestinationSectionAdmin(admin.ModelAdmin):
    list_display = [
        "destination",
        "section_title",
        "section_type",
        "order",
        "is_active",
    ]
    list_filter = ["destination", "section_type", "is_active"]
    search_fields = ["section_title", "section_content"]
    list_editable = ["order", "is_active"]
    ordering = ["destination", "order"]


@admin.register(TuitionTable)
class TuitionTableAdmin(admin.ModelAdmin):
    list_display = [
        "destination",
        "program_name",
        "program_level",
        "tuition_fee_min",
        "duration_years",
    ]
    list_filter = ["destination", "program_level"]
    search_fields = ["program_name"]
    list_editable = ["program_level", "tuition_fee_min"]


@admin.register(IntakeTable)
class IntakeTableAdmin(admin.ModelAdmin):
    list_display = [
        "destination",
        "intake_name",
        "intake_month",
        "application_deadline",
        "is_main_intake",
    ]
    list_filter = ["destination", "is_main_intake"]
    search_fields = ["intake_name"]
    list_editable = ["intake_month", "application_deadline"]


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = [
        "destination",
        "scholarship_title",
        "scholarship_type",
        "amount",
        "is_active",
    ]
    list_filter = ["destination", "scholarship_type", "is_active"]
    search_fields = ["scholarship_title"]
    list_editable = ["is_active"]


@admin.register(VisaRequirement)
class VisaRequirementAdmin(admin.ModelAdmin):
    list_display = [
        "destination",
        "visa_name",
        "visa_type",
        "processing_time",
        "visa_fee",
    ]
    list_filter = ["destination", "visa_type"]
    search_fields = ["visa_name"]
    list_editable = ["visa_type"]


@admin.register(PostStudyWork)
class PostStudyWorkAdmin(admin.ModelAdmin):
    list_display = ["destination", "visa_name", "duration"]
    list_filter = ["destination"]
    search_fields = ["visa_name"]
