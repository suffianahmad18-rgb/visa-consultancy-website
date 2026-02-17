# applications/admin.py
from django.contrib import admin
from .models import Application, Document

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ('uploaded_at',)
    can_delete = False

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'client', 'destination_country', 'status', 
                    'submitted_date', 'assigned_staff')
    list_filter = ('status', 'destination_country', 'submitted_date')
    search_fields = ('application_id', 'client__username', 'client__email')
    readonly_fields = ('application_id', 'submitted_date', 'last_updated')
    inlines = [DocumentInline]
    list_per_page = 20

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('application', 'document_type', 'verified', 'uploaded_at')
    list_filter = ('verified', 'document_type', 'uploaded_at')
    search_fields = ('application__application_id',)
    readonly_fields = ('uploaded_at',)