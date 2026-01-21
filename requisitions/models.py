from django.db import models
from django.conf import settings
from inventory.models import Product
from vendors.models import Vendor
import uuid
from datetime import datetime

class Requisition(models.Model):
    """Requisition/Purchase Request"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requisition_number = models.CharField(max_length=50, unique=True, editable=False,
                                          help_text="Auto-generated: EEL/YEAR/NUMBER")
    requisition_date = models.DateField(help_text="Date of requisition")
    remarks = models.TextField(blank=True, help_text="Additional notes")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name='requisitions_created',
                                    help_text="User who created this requisition")
    is_assigned = models.BooleanField(default=False,
                                      help_text="Whether vendors are assigned")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'requisitions'
        ordering = ['-requisition_number']
        verbose_name = 'Requisition'
        verbose_name_plural = 'Requisitions'

    def save(self, *args, **kwargs):
        if not self.requisition_number:
            # Generate: EEL/2026/001
            year = datetime.now().year
            last_req = Requisition.objects.filter(
                requisition_number__startswith=f'EEL/{year}/'
            ).order_by('-requisition_number').first()

            if last_req:
                last_num = int(last_req.requisition_number.split('/')[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.requisition_number = f'EEL/{year}/{new_num:03d}'

        super().save(*args, **kwargs)

    def __str__(self):
        return self.requisition_number


class RequisitionItem(models.Model):
    """Items in a requisition"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE,
                                     related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2,
                                   help_text="Required quantity")
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'requisition_items'
        verbose_name = 'Requisition Item'
        verbose_name_plural = 'Requisition Items'

    def __str__(self):
        return f"{self.requisition.requisition_number} - {self.product.item_name}"


class VendorRequisitionAssignment(models.Model):
    """Vendor assignment to requisition"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requisition = models.ForeignKey(Requisition, on_delete=models.PROTECT,
                                     help_text="Reference requisition")
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,
                               help_text="Assigned vendor")
    assignment_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                     help_text="User who made the assignment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendor_requisition_assignments'
        ordering = ['-created_at']
        verbose_name = 'Vendor Assignment'
        verbose_name_plural = 'Vendor Assignments'

    def __str__(self):
        return f"{self.requisition.requisition_number} - {self.vendor.vendor_name}"


class VendorRequisitionItem(models.Model):
    """Items assigned to vendor"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(VendorRequisitionAssignment, on_delete=models.CASCADE,
                                    related_name='items')
    requisition_item = models.ForeignKey(RequisitionItem, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'vendor_requisition_items'
        verbose_name = 'Vendor Item'
        verbose_name_plural = 'Vendor Items'

    def __str__(self):
        return f"{self.assignment} - {self.product.item_name}"
