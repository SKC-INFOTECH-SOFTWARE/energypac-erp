from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel
from inventory.models import GoodsReceiptNote, GoodsReceiptItem
from items.models import Item


class RejectionReason(UUIDModel, TimeStampedModel, StatusModel):
    """
    Master for rejection reasons used during quality inspection.
    """

    code = models.CharField(
        max_length=50,
        unique=True
    )

    description = models.CharField(
        max_length=255
    )

    class Meta:
        db_table = "qc_rejection_reasons"
        verbose_name = "Rejection Reason"
        verbose_name_plural = "Rejection Reasons"

    def __str__(self):
        return self.description


class QualityInspection(UUIDModel, TimeStampedModel, StatusModel):
    """
    Quality Inspection against a GRN.
    """

    grn = models.OneToOneField(
        GoodsReceiptNote,
        on_delete=models.CASCADE,
        related_name="quality_inspection"
    )

    inspection_date = models.DateField()

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "quality_inspections"
        verbose_name = "Quality Inspection"
        verbose_name_plural = "Quality Inspections"

    def __str__(self):
        return f"QC - {self.grn.grn_number}"


class QualityInspectionItem(UUIDModel, TimeStampedModel):
    """
    Item-level QC results.
    """

    inspection = models.ForeignKey(
        QualityInspection,
        on_delete=models.CASCADE,
        related_name="items"
    )

    grn_item = models.ForeignKey(
        GoodsReceiptItem,
        on_delete=models.PROTECT,
        related_name="qc_items"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="qc_items"
    )

    received_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3
    )

    accepted_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3
    )

    rejected_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3
    )

    rejection_reason = models.ForeignKey(
        RejectionReason,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="qc_items"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "quality_inspection_items"
        verbose_name = "Quality Inspection Item"
        verbose_name_plural = "Quality Inspection Items"

    def __str__(self):
        return f"{self.inspection.grn.grn_number} - {self.item.code}"
