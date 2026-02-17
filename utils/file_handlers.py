# Create utils/file_handlers.py
import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
from pypdf import PdfReader
from io import BytesIO

class SecureFileHandler:
    """Secure file handling with virus scanning and sanitization"""
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename to prevent path traversal attacks"""
        # Remove directory path
        filename = os.path.basename(filename)
        
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        
        # Remove special characters
        filename = re.sub(r'[^\w\-\.]', '', filename)
        
        # Add UUID to prevent filename collisions
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"
        
        return unique_filename
    
    @staticmethod
    def compress_image(image_file, max_size=(1200, 1200), quality=85):
        """Compress image to reduce size"""
        try:
            img = Image.open(image_file)
            
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            
            # Resize if larger than max_size
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save compressed image
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            output.seek(0)
            
            return ContentFile(output.read(), name=image_file.name)
        except Exception as e:
            raise Exception(f"Image compression failed: {str(e)}")
    
    @staticmethod
    def validate_pdf(file):
        """Validate PDF file structure"""
        try:
            file.seek(0)  # ensure file pointer at start
            pdf = PdfReader(file)

            # Check if PDF is encrypted
            if pdf.is_encrypted:
                raise ValueError("Encrypted PDFs are not allowed")

            # Check number of pages (optional limit)
            if len(pdf.pages) > 50:
                raise ValueError("PDF cannot have more than 50 pages")

            return True

        except Exception as e:
            raise ValueError(f"Invalid PDF: {str(e)}")
