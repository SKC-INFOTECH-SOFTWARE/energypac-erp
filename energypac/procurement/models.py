from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel
from items.models import Item
from masters.models import Department


class PurchaseRequisition(UUIDModel, TimeStampedModel, StatusModel):
    """
    Purchase Requisition (PR).
    Represents an internal request to procure items.
    """

    pr_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique PR reference number"
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="purchase_requisitions"
    )

    required_date = models.DateField()

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "purchase_requisitions"
        verbose_name = "Purchase Requisition"
        verbose_name_plural = "Purchase Requisitions"

    def __str__(self):
        return self.pr_number


class PurchaseRequisitionItem(UUIDModel, TimeStampedModel):
    """
    Line items for a Purchase Requisition.
    """

    purchase_requisition = models.ForeignKey(
        PurchaseRequisition,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="purchase_requisition_items"
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "purchase_requisition_items"
        verbose_name = "Purchase Requisition Item"
        verbose_name_plural = "Purchase Requisition Items"

    def __str__(self):
        return f"{self.purchase_requisition.pr_number} - {self.item.code}"


class PurchaseOrder(UUIDModel, TimeStampedModel, StatusModel):
    """
    Purchase Order (PO).
    Represents a confirmed order placed to a vendor.
    """

    po_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique PO reference number"
    )

    pr = models.ForeignKey(
        PurchaseRequisition,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="purchase_orders"
    )

    order_date = models.DateField()

    delivery_date = models.DateField(null=True, blank=True)

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "purchase_orders"
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    def __str__(self):
        return self.po_number


class PurchaseOrderItem(UUIDModel, TimeStampedModel):
    """
    Line items for a Purchase Order.
    """

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="purchase_order_items"
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3
    )

    rate = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        db_table = "purchase_order_items"
        verbose_name = "Purchase Order Item"
        verbose_name_plural = "Purchase Order Items"

    def __str__(self):
        return f"{self.purchase_order.po_number} - {self.item.code}"
