from django.db import models
import uuid

class Product(models.Model):
    """Product Master - Items/Products in inventory"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item_code = models.CharField(max_length=50, unique=True,
                                  help_text="Unique item code")
    item_name = models.CharField(max_length=200,
                                  help_text="Product/Item name")
    description = models.TextField(blank=True,
                                    help_text="Detailed description")
    hsn_code = models.CharField(max_length=20, blank=True,
                                 help_text="HSN/SAC code for GST")
    unit = models.CharField(max_length=20, default='PCS',
                           help_text="Unit of measurement (PCS, KG, LTR, MTR, etc.)")
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        help_text="Current stock quantity")
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        help_text="Minimum stock level")
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                               help_text="Price per unit")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"{self.item_code} - {self.item_name}"
