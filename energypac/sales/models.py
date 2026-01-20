from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel
from items.models import Item


class SalesQuotation(UUIDModel, TimeStampedModel, StatusModel):
    """
    Sales Quotation.
    Represents an offer made to a customer.
    """

    quotation_number = models.CharField(
        max_length=50,
        unique=True
    )

    quotation_date = models.DateField()

    customer_name = models.CharField(
        max_length=255,
        help_text="Customer name (customer master can be added later)"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "sales_quotations"
        verbose_name = "Sales Quotation"
        verbose_name_plural = "Sales Quotations"

    def __str__(self):
        return self.quotation_number


class SalesQuotationItem(UUIDModel, TimeStampedModel):
    """
    Line items for Sales Quotation.
    """

    quotation = models.ForeignKey(
        SalesQuotation,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="sales_quotation_items"
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
        db_table = "sales_quotation_items"
        verbose_name = "Sales Quotation Item"
        verbose_name_plural = "Sales Quotation Items"

    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.item.code}"


class SalesOrder(UUIDModel, TimeStampedModel, StatusModel):
    """
    Sales Order.
    Represents a confirmed customer order.
    """

    order_number = models.CharField(
        max_length=50,
        unique=True
    )

    quotation = models.ForeignKey(
        SalesQuotation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sales_orders"
    )

    order_date = models.DateField()

    customer_name = models.CharField(
        max_length=255
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "sales_orders"
        verbose_name = "Sales Order"
        verbose_name_plural = "Sales Orders"

    def __str__(self):
        return self.order_number


class SalesOrderItem(UUIDModel, TimeStampedModel):
    """
    Line items for Sales Order.
    """

    order = models.ForeignKey(
        SalesOrder,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="sales_order_items"
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
        db_table = "sales_order_items"
        verbose_name = "Sales Order Item"
        verbose_name_plural = "Sales Order Items"

    def __str__(self):
        return f"{self.order.order_number} - {self.item.code}"


class SalesInvoice(UUIDModel, TimeStampedModel, StatusModel):
    """
    Sales Invoice.
    Represents billing to customer.
    """

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    order = models.ForeignKey(
        SalesOrder,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invoices"
    )

    invoice_date = models.DateField()

    customer_name = models.CharField(
        max_length=255
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "sales_invoices"
        verbose_name = "Sales Invoice"
        verbose_name_plural = "Sales Invoices"

    def __str__(self):
        return self.invoice_number


class SalesInvoiceItem(UUIDModel, TimeStampedModel):
    """
    Line items for Sales Invoice.
    """

    invoice = models.ForeignKey(
        SalesInvoice,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="sales_invoice_items"
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
        db_table = "sales_invoice_items"
        verbose_name = "Sales Invoice Item"
        verbose_name_plural = "Sales Invoice Items"

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.item.code}"
