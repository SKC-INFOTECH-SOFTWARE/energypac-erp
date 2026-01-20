from django.db import models

from core.models import UUIDModel, TimeStampedModel, StatusModel
from masters.models import UnitOfMeasure


class ItemType(models.TextChoices):
    """
    Item classification.
    """
    RAW_MATERIAL = "RAW", "Raw Material"
    FINISHED_GOOD = "FINISHED", "Finished Good"
    SEMI_FINISHED = "SEMI", "Semi Finished"
    SERVICE = "SERVICE", "Service"
    CONSUMABLE = "CONSUMABLE", "Consumable"


class Item(UUIDModel, TimeStampedModel, StatusModel):
    """
    Item master.
    Represents any material, product, or service in the ERP.
    """

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique item code / SKU"
    )

    name = models.CharField(
        max_length=255,
        help_text="Item name or description"
    )

    item_type = models.CharField(
        max_length=20,
        choices=ItemType.choices
    )

    uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        related_name="items"
    )

    description = models.TextField(blank=True)

    class Meta:
        db_table = "items"
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.code} - {self.name}"
