from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models 
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Product CRUD operations

    list: Get all products
    create: Add new product
    retrieve: Get product by ID
    update: Update product
    partial_update: Partially update product
    destroy: Delete product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'unit']
    search_fields = ['item_code', 'item_name', 'hsn_code', 'description']
    ordering_fields = ['item_name', 'created_at', 'current_stock', 'rate']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get products below reorder level"""
        low_stock_products = self.queryset.filter(
            current_stock__lte=models.F('reorder_level'),
            is_active=True
        )
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active products"""
        active_products = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_products, many=True)
        return Response(serializer.data)
