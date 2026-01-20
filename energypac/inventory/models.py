from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel
from items.models import Item
from masters.models import Warehouse
from procurement.models import PurchaseOrder


class GoodsReceiptNote(UUIDModel, TimeStampedModel, StatusModel):
    """
    Goods Receipt Note (GRN).
    Represents receipt of goods into inventory.
    """

    grn_number = models.CharField(
        max_length=50, unique=True, help_text="Unique GRN reference number"
    )

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="grns",
    )

    received_date = models.DateField()

    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="grns"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "goods_receipt_notes"
        verbose_name = "Goods Receipt Note"
        verbose_name_plural = "Goods Receipt Notes"

    def __str__(self):
        return self.grn_number


class GoodsReceiptItem(UUIDModel, TimeStampedModel):
    """
    Line items for a Goods Receipt Note.
    """

    grn = models.ForeignKey(
        GoodsReceiptNote, on_delete=models.CASCADE, related_name="items"
    )

    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="grn_items")

    quantity = models.DecimalField(max_digits=12, decimal_places=3)

    class Meta:
        db_table = "goods_receipt_items"
        verbose_name = "Goods Receipt Item"
        verbose_name_plural = "Goods Receipt Items"

    def __str__(self):
        return f"{self.grn.grn_number} - {self.item.code}"


class StockLedger(UUIDModel, TimeStampedModel):
    """
    Stock Ledger.
    Every stock movement (IN / OUT) creates one ledger entry.
    """

    class MovementType(models.TextChoices):
        IN = "IN", "Stock In"
        OUT = "OUT", "Stock Out"

    item = models.ForeignKey(
        Item, on_delete=models.PROTECT, related_name="stock_ledger_entries"
    )

    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="stock_ledger_entries"
    )

    movement_type = models.CharField(max_length=10, choices=MovementType.choices)

    quantity = models.DecimalField(max_digits=12, decimal_places=3)

    reference_type = models.CharField(
        max_length=50, help_text="Source document type (GRN, Issue, Adjustment, etc.)"
    )

    reference_id = models.UUIDField(help_text="UUID of the source document")

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "stock_ledger"
        verbose_name = "Stock Ledger"
        verbose_name_plural = "Stock Ledger"
        indexes = [
            models.Index(fields=["item", "warehouse"]),
            models.Index(fields=["reference_type", "reference_id"]),
        ]

    def __str__(self):
        return f"{self.item.code} | {self.movement_type} | {self.quantity}"
