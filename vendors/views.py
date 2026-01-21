from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Vendor
from .serializers import VendorSerializer

class VendorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vendor CRUD operations

    list: Get all vendors
    create: Add new vendor
    retrieve: Get vendor by ID
    update: Update vendor
    partial_update: Partially update vendor
    destroy: Delete vendor
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['vendor_code', 'vendor_name', 'contact_person',
                     'gst_number', 'pan_number']
    ordering_fields = ['vendor_name', 'created_at']
    ordering = ['vendor_name']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get only active vendors"""
        active_vendors = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_vendors, many=True)
        return Response(serializer.data)
