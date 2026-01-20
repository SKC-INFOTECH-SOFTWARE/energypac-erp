from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from core.models import UUIDModel, TimeStampedModel
from masters.models import Role, Department


class User(AbstractUser, UUIDModel, TimeStampedModel):
    """
    Custom User model for ERP.
    Identity is employee_code based.
    """

    employee_code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique employee code used for login"
    )

    # Business role mapping (ERP role master)
    roles = models.ManyToManyField(
        Role,
        related_name="users",
        blank=True
    )

    # Organizational mapping
    department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users"
    )

    # Override Django auth relations to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name="erp_users",
        blank=True,
        help_text="Django auth groups (admin use only)"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="erp_users",
        blank=True,
        help_text="Django auth permissions (admin use only)"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.employee_code} - {self.get_full_name() or self.username}"
