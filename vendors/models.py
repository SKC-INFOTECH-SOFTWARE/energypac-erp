from django.db import models
import uuid

class Vendor(models.Model):
    """Vendor Master - Supplier information"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_code = models.CharField(max_length=50, unique=True,
                                    help_text="Unique vendor code")
    vendor_name = models.CharField(max_length=200,
                                    help_text="Vendor/Supplier name")
    contact_person = models.CharField(max_length=100, blank=True,
                                      help_text="Primary contact person")
    phone = models.CharField(max_length=15, blank=True,
                            help_text="Contact phone number")
    email = models.EmailField(blank=True,
                              help_text="Contact email")
    address = models.TextField(blank=True,
                               help_text="Complete address")
    gst_number = models.CharField(max_length=50, blank=True,
                                  help_text="GST registration number")
    pan_number = models.CharField(max_length=50, blank=True,
                                  help_text="PAN number")
    bank_name = models.CharField(max_length=100, blank=True)
    bank_account_number = models.CharField(max_length=50, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vendors'
        ordering = ['vendor_name']
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        return f"{self.vendor_code} - {self.vendor_name}"
