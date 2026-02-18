from django import forms

from study_destinations.models import StudyDestination
from utils.file_handlers import SecureFileHandler

from .models import Application, Document


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            # Personal info
            "full_name",
            "phone_number",
            "email",
            # Education
            "last_qualification",
            "grade_marks",
            "completion_year",
            # Destination
            "destination",
            "destination_country",
            "preferred_course",
            # English test
            "english_test",
            "english_score",
            # Visa history
            "visa_refusal",
            "visa_refusal_details",
        ]
        widgets = {
            # Personal info
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your full name"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "+92 300 1234567"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "your@email.com"}),
            # Education
            "last_qualification": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Bachelor of Science",
                }
            ),
            "grade_marks": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., 85%, GPA 3.5"}),
            "completion_year": forms.NumberInput(attrs={"class": "form-control", "placeholder": "2024"}),
            # Destination
            "destination_country": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "destination": forms.Select(attrs={"class": "form-control"}),
            "preferred_course": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., MS in Computer Science",
                }
            ),
            # English test
            "english_test": forms.Select(attrs={"class": "form-control"}),
            "english_score": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., IELTS 6.5 bands"}),
            # Visa history
            "visa_refusal": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "visa_refusal_details": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": "form-control",
                    "placeholder": "If yes, please provide details...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show published destinations
        self.fields["destination"].queryset = StudyDestination.objects.filter(is_published=True)
        self.fields["destination"].label_from_instance = (
            lambda obj: f"{obj.country_name} - {obj.get_country_code_display()}"
        )
        self.fields["destination"].empty_label = "Select Study Destination"

        # Make visa_refusal_details optional but required if visa_refusal is True
        self.fields["visa_refusal_details"].required = False

    def clean(self):
        cleaned_data = super().clean()
        visa_refusal = cleaned_data.get("visa_refusal")
        visa_refusal_details = cleaned_data.get("visa_refusal_details")

        # If visa refusal is checked, details must be provided
        if visa_refusal and not visa_refusal_details:
            self.add_error("visa_refusal_details", "Please provide details about your visa refusal")

        return cleaned_data


class ApplicationStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status", "notes", "assigned_staff"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "assigned_staff": forms.Select(attrs={"class": "form-control"}),
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["document_type", "file"]
        widgets = {
            "document_type": forms.Select(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean_file(self):
        file = self.cleaned_data.get("file")

        if file:
            # Check file size (max 10MB)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be less than 10MB")

            # Check file extension
            import os

            ext = os.path.splitext(file.name)[1].lower()
            allowed_extensions = [".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"]
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"File type {ext} not allowed. Allowed: {', '.join(allowed_extensions)}")

        return file
