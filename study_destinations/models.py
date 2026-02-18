# study_destinations/models.py
from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class StudyDestination(models.Model):
    COUNTRY_CHOICES = [
        ("UK", "United Kingdom"),
        ("USA", "United States"),
        ("CANADA", "Canada"),
        ("AUSTRALIA", "Australia"),
        ("GERMANY", "Germany"),
        ("FRANCE", "France"),
        ("NETHERLANDS", "Netherlands"),
        ("IRELAND", "Ireland"),
        ("NEW_ZEALAND", "New Zealand"),
        ("OTHER", "Other"),
    ]

    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default="OTHER")
    slug = models.SlugField(unique=True, max_length=100)
    banner_image = models.ImageField(upload_to="study_destinations/banners/")
    intro_title = models.CharField(max_length=200)
    intro_description = RichTextField()

    # Quick facts
    quick_fact_1 = models.CharField(max_length=100, blank=True)
    quick_fact_2 = models.CharField(max_length=100, blank=True)
    quick_fact_3 = models.CharField(max_length=100, blank=True)
    quick_fact_4 = models.CharField(max_length=100, blank=True)

    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    # Status
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Lower number appears first")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "country_name"]
        verbose_name = "Study Destination"
        verbose_name_plural = "Study Destinations"

    def __str__(self):
        return self.country_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.country_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("study_destinations:detail", kwargs={"slug": self.slug})

    def get_flag_emoji(self):
        flag_map = {
            "UK": "🇬🇧",
            "USA": "🇺🇸",
            "CANADA": "🇨🇦",
            "AUSTRALIA": "🇦🇺",
            "GERMANY": "🇩🇪",
            "FRANCE": "🇫🇷",
            "NETHERLANDS": "🇳🇱",
            "IRELAND": "🇮🇪",
            "NEW_ZEALAND": "🇳🇿",
        }
        return flag_map.get(self.country_code, "🌍")


class DestinationSection(models.Model):
    SECTION_TYPES = [
        ("WHY_STUDY", "Why Study Here"),
        ("EDUCATION_SYSTEM", "Education System"),
        ("COST_LIVING", "Cost of Living"),
        ("ACCOMMODATION", "Accommodation"),
        ("WORK_RIGHTS", "Work Rights"),
        ("HEALTHCARE", "Healthcare System"),
        ("CULTURE", "Culture & Lifestyle"),
        ("ADMISSION_PROCESS", "Admission Process"),
        ("LANGUAGE", "Language Requirements"),
        ("OTHER", "Other"),
    ]

    destination = models.ForeignKey(StudyDestination, on_delete=models.CASCADE, related_name="sections")
    section_title = models.CharField(max_length=200)
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, default="OTHER")
    section_content = RichTextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "section_title"]

    def __str__(self):
        return f"{self.destination.country_name} - {self.section_title}"


class TuitionTable(models.Model):
    PROGRAM_LEVELS = [
        ("UNDERGRADUATE", "Undergraduate"),
        ("POSTGRADUATE", "Postgraduate"),
        ("PHD", "PhD/Doctoral"),
        ("DIPLOMA", "Diploma"),
        ("FOUNDATION", "Foundation Program"),
        ("LANGUAGE", "Language Course"),
    ]

    destination = models.ForeignKey(StudyDestination, on_delete=models.CASCADE, related_name="tuition_fees")
    program_name = models.CharField(max_length=200)
    program_level = models.CharField(max_length=50, choices=PROGRAM_LEVELS, default="UNDERGRADUATE")
    tuition_fee_min = models.DecimalField(max_digits=10, decimal_places=2, help_text="Minimum annual fee in USD")
    tuition_fee_max = models.DecimalField(max_digits=10, decimal_places=2, help_text="Maximum annual fee in USD")
    duration_years = models.CharField(max_length=50, help_text="e.g., 3-4 years, 1-2 years")
    notes = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "program_level", "program_name"]
        verbose_name = "Tuition Fee"
        verbose_name_plural = "Tuition Fees"

    def __str__(self):
        return f"{self.destination.country_name} - {self.program_name}"


class IntakeTable(models.Model):
    destination = models.ForeignKey(StudyDestination, on_delete=models.CASCADE, related_name="intakes")
    intake_name = models.CharField(max_length=100)
    intake_month = models.CharField(max_length=50, help_text="e.g., September, January, May")
    application_deadline = models.CharField(max_length=100, help_text="e.g., 3-6 months before intake")
    visa_deadline = models.CharField(max_length=100, blank=True, help_text="Latest visa application date")
    is_main_intake = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "intake_name"]

    def __str__(self):
        return f"{self.destination.country_name} - {self.intake_name}"


class Scholarship(models.Model):
    SCHOLARSHIP_TYPES = [
        ("MERIT", "Merit-based"),
        ("NEED", "Need-based"),
        ("GOVERNMENT", "Government Scholarship"),
        ("UNIVERSITY", "University Scholarship"),
        ("EXTERNAL", "External/Private"),
        ("SPORTS", "Sports Scholarship"),
        ("RESEARCH", "Research Grant"),
    ]

    destination = models.ForeignKey(StudyDestination, on_delete=models.CASCADE, related_name="scholarships")
    scholarship_title = models.CharField(max_length=200)
    scholarship_type = models.CharField(max_length=50, choices=SCHOLARSHIP_TYPES, default="MERIT")
    amount = models.CharField(max_length=200, help_text="e.g., $10,000, Full Tuition, 50% off")
    eligibility = RichTextField()
    application_deadline = models.CharField(max_length=100, blank=True)
    website_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "scholarship_title"]

    def __str__(self):
        return f"{self.destination.country_name} - {self.scholarship_title}"


class VisaRequirement(models.Model):
    VISA_TYPES = [
        ("STUDENT", "Student Visa"),
        ("WORK_PERMIT", "Work Permit"),
        ("POST_STUDY", "Post-Study Work Visa"),
        ("TOURIST", "Tourist Visa"),
        ("DEPENDENT", "Dependent Visa"),
    ]

    destination = models.ForeignKey(StudyDestination, on_delete=models.CASCADE, related_name="visa_requirements")
    visa_type = models.CharField(max_length=50, choices=VISA_TYPES, default="STUDENT")
    visa_name = models.CharField(max_length=200, help_text="e.g., Tier 4 (General) Student Visa")
    processing_time = models.CharField(max_length=100, help_text="e.g., 3-8 weeks")
    visa_fee = models.CharField(max_length=100, help_text="e.g., $350")
    financial_requirement = models.CharField(max_length=200, help_text="e.g., Proof of $15,000 minimum")
    documents_required = RichTextField()
    eligibility_criteria = RichTextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "visa_type"]
        verbose_name = "Visa Requirement"
        verbose_name_plural = "Visa Requirements"

    def __str__(self):
        return f"{self.destination.country_name} - {self.visa_name}"


class PostStudyWork(models.Model):
    destination = models.ForeignKey(StudyDestination, on_delete=models.CASCADE, related_name="post_study_work")
    visa_name = models.CharField(max_length=200, help_text="e.g., Post-Study Work Visa (PSW)")
    duration = models.CharField(max_length=100, help_text="e.g., 2 years, 3 years")
    eligibility = RichTextField(help_text="Who can apply?")
    application_process = RichTextField()
    work_rights = RichTextField(help_text="What type of work is allowed?")
    pathway_to_pr = RichTextField(blank=True, help_text="Pathway to Permanent Residency")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Post-Study Work Option"
        verbose_name_plural = "Post-Study Work Options"

    def __str__(self):
        return f"{self.destination.country_name} - {self.visa_name}"
