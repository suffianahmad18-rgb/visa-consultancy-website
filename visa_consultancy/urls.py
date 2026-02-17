# visa_consultancy/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('dashboard/', include('applications.urls', namespace='dashboard')),
    path('study-destinations/', include('study_destinations.urls', namespace='study_destinations')),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('messages/', include('messaging.urls', namespace='messaging')),
    path('testimonials/', include('testimonials.urls', namespace='testimonials')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)