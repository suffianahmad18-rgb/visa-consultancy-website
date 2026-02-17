# accounts/admin.py
from django.contrib import admin
from .models import ClientProfile, StaffProfile

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'passport_number')
    list_filter = ('country', 'created_at')

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'designation', 'is_agent')
    search_fields = ('user__username', 'user__email', 'phone', 'department')
    list_filter = ('department', 'designation', 'is_agent')