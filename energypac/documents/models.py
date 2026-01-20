from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.models import UUIDModel, TimeStampedModel, StatusModel


class DocumentType(UUIDModel, TimeStampedModel, StatusModel):
    """
    Master for document types.
    Example: Purchase Order, Invoice, Packing List, LC Copy, QC Report
    """

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "document_types"
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"

    def __str__(self):
        return self.name


class Document(UUIDModel, TimeStampedModel):
    """
    Stores uploaded document metadata.
    Actual storage backend handled elsewhere.
    """

    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.PROTECT,
        related_name="documents"
    )

    file = models.FileField(
        upload_to="documents/"
    )

    original_filename = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(blank=True)

    class Meta:
        db_table = "documents"
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.original_filename or str(self.id)


class DocumentLink(UUIDModel, TimeStampedModel):
    """
    Generic link between a document and any ERP object.
    """

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="links"
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.UUIDField()
    content_object = GenericForeignKey(
        "content_type",
        "object_id"
    )

    class Meta:
        db_table = "document_links"
        verbose_name = "Document Link"
        verbose_name_plural = "Document Links"
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
