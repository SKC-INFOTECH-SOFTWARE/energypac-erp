from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_code', 'vendor_name', 'contact_person', 'phone',
                    'email', 'gst_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['vendor_code', 'vendor_name', 'contact_person',
                     'gst_number', 'pan_number']
    ordering = ['vendor_name']
    list_per_page = 50
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('vendor_code', 'vendor_name', 'contact_person')
        }),
        ('Contact Details', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Tax Information', {
            'fields': ('gst_number', 'pan_number')
        }),
        ('Banking Details', {
            'fields': ('bank_name', 'bank_account_number', 'ifsc_code'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
