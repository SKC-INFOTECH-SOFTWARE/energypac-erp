from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['item_code', 'item_name', 'hsn_code', 'unit',
                    'current_stock', 'reorder_level', 'rate', 'is_active', 'created_at']
    list_filter = ['is_active', 'unit', 'created_at']
    search_fields = ['item_code', 'item_name', 'hsn_code', 'description']
    ordering = ['-created_at']
    list_per_page = 50
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('item_code', 'item_name', 'description')
        }),
        ('Classification', {
            'fields': ('hsn_code', 'unit')
        }),
        ('Stock & Pricing', {
            'fields': ('current_stock', 'reorder_level', 'rate')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
