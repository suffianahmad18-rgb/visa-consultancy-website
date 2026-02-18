# messaging/urls.py
from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    # Regular user URLs
    path("", views.InboxView.as_view(), name="inbox"),
    path("sent/", views.SentView.as_view(), name="sent"),
    path("compose/", views.ComposeMessageView.as_view(), name="compose"),
    path("<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"),
    # Admin URLs
    path("admin/inbox/", views.AdminInboxView.as_view(), name="admin_inbox"),
    path(
        "admin/message/<int:pk>/",
        views.AdminMessageDetailView.as_view(),
        name="admin_message_detail",
    ),
]
