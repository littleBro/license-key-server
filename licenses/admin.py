from django.contrib import admin
from .models import LicenseKey


@admin.register(LicenseKey)
class LicenseKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'employee_name', 'is_active', 'last_used')
    readonly_fields = ('last_used',)
