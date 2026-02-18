# testimonials/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class Testimonial(models.Model):
    CATEGORY_CHOICES = [
        ("STUDY_VISA", "Study Visa"),
    ]

    COUNTRY_CHOICES = [
        ("USA", "United States"),
        ("UK", "United Kingdom"),
        ("CANADA", "Canada"),
        ("AUSTRALIA", "Australia"),
        ("GERMANY", "Germany"),
        ("FRANCE", "France"),
        ("JAPAN", "Japan"),
        ("SINGAPORE", "Singapore"),
        ("UAE", "United Arab Emirates"),
        ("OTHER", "Other"),
    ]

    client_name = models.CharField(max_length=200)
    client_image = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES)
    visa_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    university = models.CharField(max_length=200, blank=True)  # For study visa testimonials
    course = models.CharField(max_length=200, blank=True)  # For study visa testimonials
    testimonial_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.get_visa_category_display()}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonials")

    def stars(self):
        """Return HTML for rating stars"""
        return "★" * self.rating + "☆" * (5 - self.rating)
