# messaging/models.py
from django.contrib.auth.models import User
from django.db import models

from applications.models import Application


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="messages",
        null=True,
        blank=True,
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}: {self.subject}"
