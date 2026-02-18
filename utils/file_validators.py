# Create utils/file_validators.py
import os

import magic
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible


@deconstructible
class FileValidator:
    """
    Validates files for:
    - Maximum size
    - Allowed extensions
    - MIME types
    """

    def __init__(self, max_size=None, allowed_extensions=None, allowed_mime_types=None):
        self.max_size = max_size
        self.allowed_extensions = allowed_extensions or []
        self.allowed_mime_types = allowed_mime_types or []

    def __call__(self, value):
        # Check file size
        if self.max_size and value.size > self.max_size:
            raise ValidationError(
                f"File size must not exceed {filesizeformat(self.max_size)}. "
                f"Current file size is {filesizeformat(value.size)}."
            )

        # Check file extension
        ext = os.path.splitext(value.name)[1].lower()
        if self.allowed_extensions and ext not in self.allowed_extensions:
            raise ValidationError(
                f'File extension "{ext}" is not allowed. ' f'Allowed extensions: {", ".join(self.allowed_extensions)}'
            )

        # Check MIME type (using python-magic)
        try:
            mime = magic.Magic(mime=True)
            file_mime_type = mime.from_buffer(value.read(1024))
            value.seek(0)  # Reset file pointer

            if self.allowed_mime_types and file_mime_type not in self.allowed_mime_types:
                raise ValidationError(
                    f'File type "{file_mime_type}" is not allowed. '
                    f'Allowed file types: {", ".join(self.allowed_mime_types)}'
                )
        except ImportError:
            # python-magic not installed, skip MIME validation
            pass
        except Exception as e:
            raise ValidationError(f"Error validating file type: {str(e)}")

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator)
            and self.max_size == other.max_size
            and self.allowed_extensions == other.allowed_extensions
            and self.allowed_mime_types == other.allowed_mime_types
        )


# Update applications/models.py
from utils.file_validators import FileValidator


class Document(models.Model):
    # ... existing fields ...

    # Add file field with validation
    file = models.FileField(
        upload_to="application_documents/",
        validators=[
            FileValidator(
                max_size=10 * 1024 * 1024,  # 10MB
                allowed_extensions=[".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"],
                allowed_mime_types=[
                    "application/pdf",
                    "image/jpeg",
                    "image/png",
                    "image/jpg",
                    "application/msword",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ],
            )
        ],
    )
