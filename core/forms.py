# core/forms.py
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Full Name"}),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email Address"})
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Phone Number"}),
    )

    subject = forms.ChoiceField(
        choices=[
            ("general", "General Inquiry"),
            ("visa_consultation", "Visa Consultation"),
            ("study_visa", "Study Visa - Gujranwala Students"),
            ("application_status", "Application Status"),
            ("document_help", "Document Assistance"),
            ("appointment", "Book Appointment"),
            ("complaint", "Complaint"),
            ("other", "Other"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Your message here...",
            }
        )
    )

    newsletter = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
