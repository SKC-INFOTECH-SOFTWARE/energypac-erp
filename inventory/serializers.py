from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model"""

    class Meta:
        model = Product
        fields = [
            'id', 'item_code', 'item_name', 'description', 'hsn_code',
            'unit', 'current_stock', 'reorder_level', 'rate', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_item_code(self, value):
        """Ensure item code is unique"""
        if self.instance:  # Update operation
            if Product.objects.exclude(pk=self.instance.pk).filter(item_code=value).exists():
                raise serializers.ValidationError("Item code already exists")
        else:  # Create operation
            if Product.objects.filter(item_code=value).exists():
                raise serializers.ValidationError("Item code already exists")
        return value.upper()
