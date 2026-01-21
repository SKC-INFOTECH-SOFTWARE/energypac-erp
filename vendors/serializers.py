from rest_framework import serializers
from .models import Vendor

class VendorSerializer(serializers.ModelSerializer):
    """Serializer for Vendor model"""

    class Meta:
        model = Vendor
        fields = [
            'id', 'vendor_code', 'vendor_name', 'contact_person', 'phone',
            'email', 'address', 'gst_number', 'pan_number', 'bank_name',
            'bank_account_number', 'ifsc_code', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_vendor_code(self, value):
        """Ensure vendor code is unique"""
        if self.instance:  # Update
            if Vendor.objects.exclude(pk=self.instance.pk).filter(vendor_code=value).exists():
                raise serializers.ValidationError("Vendor code already exists")
        else:  # Create
            if Vendor.objects.filter(vendor_code=value).exists():
                raise serializers.ValidationError("Vendor code already exists")
        return value.upper()
