# Create utils/email_service.py
import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_application_submitted(application):
        """Send email when application is submitted"""
        context = {
            'user': application.client,
            'application': application,
            'application_id': application.application_id,
            'visa_category': application.visa_category.name,
            'site_name': settings.SITE_NAME,
        }
        
        subject = f"Visa Application Submitted - {application.application_id}"
        html_content = render_to_string('emails/application_submitted.html', context)
        text_content = strip_tags(html_content)
        
        return EmailService._send_email(
            recipient=application.client.email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )
    
    @staticmethod
    def send_status_update(application, old_status, new_status):
        """Send email when application status changes"""
        context = {
            'user': application.client,
            'application': application,
            'old_status': application.get_status_display(old_status),
            'new_status': application.get_status_display(new_status),
            'site_name': settings.SITE_NAME,
        }
        
        subject = f"Application Status Updated - {application.application_id}"
        html_content = render_to_string('emails/status_updated.html', context)
        text_content = strip_tags(html_content)
        
        return EmailService._send_email(
            recipient=application.client.email,
            subject=subject,
            html_content=html_content,
            text_content=text_content
        )
    
    @staticmethod
    def _send_email(recipient, subject, html_content, text_content, cc=None):
        """Send email with HTML and plain text versions"""
        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient],
                cc=cc if cc else [],
                reply_to=[settings.DEFAULT_FROM_EMAIL]
            )
            email.attach_alternative(html_content, "text/html")
            result = email.send(fail_silently=False)
            logger.info(f"Email sent to {recipient}: {subject}")
            return result
        except Exception as e:
            logger.error(f"Failed to send email to {recipient}: {str(e)}")
            return 0

# Create signal handler for status changes
# applications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application
from utils.email_service import EmailService

@receiver(post_save, sender=Application)
def send_status_update_email(sender, instance, created, **kwargs):
    """Send email when application status changes"""
    if not created:
        try:
            # Get previous status from database
            previous = Application.objects.get(pk=instance.pk)
            if previous.status != instance.status:
                EmailService.send_status_update(instance, previous.status, instance.status)
        except Application.DoesNotExist:
            pass