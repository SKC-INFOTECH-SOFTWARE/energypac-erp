from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['employee_code', 'username', 'email', 'first_name', 'last_name',
                    'department', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'department', 'date_joined']
    search_fields = ['employee_code', 'username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('employee_code', 'phone', 'department')
        }),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('employee_code', 'phone', 'department')
        }),
    )
