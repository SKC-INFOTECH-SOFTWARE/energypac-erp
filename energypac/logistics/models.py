from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel
from items.models import Item
from masters.models import Warehouse
from sales.models import SalesOrder, SalesInvoice


class Dispatch(UUIDModel, TimeStampedModel, StatusModel):
    """
    Dispatch note.
    Represents physical dispatch of goods from warehouse.
    """

    dispatch_number = models.CharField(
        max_length=50,
        unique=True
    )

    order = models.ForeignKey(
        SalesOrder,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dispatches"
    )

    invoice = models.ForeignKey(
        SalesInvoice,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="dispatches"
    )

    dispatch_date = models.DateField()

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name="dispatches"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "dispatches"
        verbose_name = "Dispatch"
        verbose_name_plural = "Dispatches"

    def __str__(self):
        return self.dispatch_number


class DispatchItem(UUIDModel, TimeStampedModel):
    """
    Line items for Dispatch.
    """

    dispatch = models.ForeignKey(
        Dispatch,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="dispatch_items"
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3
    )

    class Meta:
        db_table = "dispatch_items"
        verbose_name = "Dispatch Item"
        verbose_name_plural = "Dispatch Items"

    def __str__(self):
        return f"{self.dispatch.dispatch_number} - {self.item.code}"


class Shipment(UUIDModel, TimeStampedModel, StatusModel):
    """
    Shipment details.
    Represents transport and delivery information.
    """

    shipment_number = models.CharField(
        max_length=50,
        unique=True
    )

    dispatches = models.ManyToManyField(
        Dispatch,
        related_name="shipments",
        blank=True
    )

    transporter_name = models.CharField(
        max_length=255
    )

    vehicle_number = models.CharField(
        max_length=50,
        blank=True
    )

    tracking_number = models.CharField(
        max_length=100,
        blank=True
    )

    shipment_date = models.DateField()
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "shipments"
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"

    def __str__(self):
        return self.shipment_number
