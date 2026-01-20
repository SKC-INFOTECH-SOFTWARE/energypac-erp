import uuid
from django.conf import settings
from django.db import models


class UUIDModel(models.Model):
    """
    Abstract base model with UUID primary key.
    Used by all ERP models.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    Abstract base model to track creation and update timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    """
    Abstract model for generic lifecycle status management.
    Business apps may extend or override statuses.
    """

    class StatusChoices(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CLOSED = "CLOSED", "Closed"

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AuditModel(models.Model):
    """
    Abstract model for user audit and approval tracking.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_approved"
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
# core/models.py

import uuid
from django.conf import settings
from django.db import models


class UUIDModel(models.Model):
    """
    Abstract base model with UUID primary key.
    Used by all ERP models.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    Abstract base model to track creation and update timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    """
    Abstract model for generic lifecycle status management.
    Business apps may extend or override statuses.
    """

    class StatusChoices(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CLOSED = "CLOSED", "Closed"

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AuditModel(models.Model):
    """
    Abstract model for user audit and approval tracking.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_approved"
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
