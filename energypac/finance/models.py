from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel
from masters.models import Bank
from sales.models import SalesInvoice


class LetterOfCredit(UUIDModel, TimeStampedModel, StatusModel):
    """
    Letter of Credit (LC).
    Represents a bank-backed payment instrument.
    """

    lc_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="LC reference number"
    )

    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        related_name="lcs"
    )

    issue_date = models.DateField()
    expiry_date = models.DateField()

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "letter_of_credits"
        verbose_name = "Letter of Credit"
        verbose_name_plural = "Letters of Credit"

    def __str__(self):
        return self.lc_number


class InvoicePayment(UUIDModel, TimeStampedModel):
    """
    Payments received against a sales invoice.
    """

    class PaymentMode(models.TextChoices):
        CASH = "CASH", "Cash"
        BANK_TRANSFER = "BANK", "Bank Transfer"
        CHEQUE = "CHEQUE", "Cheque"
        LC = "LC", "Letter of Credit"

    invoice = models.ForeignKey(
        SalesInvoice,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_date = models.DateField()

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PaymentMode.choices
    )

    bank = models.ForeignKey(
        Bank,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invoice_payments"
    )

    lc = models.ForeignKey(
        LetterOfCredit,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invoice_payments"
    )

    reference_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="Cheque number / transaction reference"
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = "invoice_payments"
        verbose_name = "Invoice Payment"
        verbose_name_plural = "Invoice Payments"

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.amount}"
