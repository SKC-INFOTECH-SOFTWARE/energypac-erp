from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Requisition, VendorRequisitionAssignment
from .serializers import (RequisitionSerializer, RequisitionCreateSerializer,
                          VendorRequisitionAssignmentSerializer,
                          VendorAssignmentCreateSerializer)

class RequisitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Requisition CRUD

    list: Get all requisitions
    create: Create new requisition with items
    retrieve: Get requisition by ID
    update: Update requisition (not allowed after assignment)
    destroy: Delete requisition (NOT ALLOWED)

    Custom actions:
    - items: Get all items for a requisition
    - assignments: Get all vendor assignments
    """
    queryset = Requisition.objects.all().select_related('created_by').prefetch_related('items__product')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_assigned', 'requisition_date', 'created_by']
    search_fields = ['requisition_number', 'remarks']
    ordering_fields = ['requisition_date', 'created_at', 'requisition_number']
    ordering = ['-requisition_number']

    def get_serializer_class(self):
        if self.action == 'create':
            return RequisitionCreateSerializer
        return RequisitionSerializer

    def perform_create(self, serializer):
        """Automatically set created_by to logged-in user"""
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Prevent deletion of requisitions"""
        return Response(
            {
                'error': 'Requisitions cannot be deleted',
                'message': 'Once created, requisitions are permanent for audit purposes'
            },
            status=status.HTTP_403_FORBIDDEN
        )

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get all items for a specific requisition"""
        requisition = self.get_object()
        from .serializers import RequisitionItemSerializer
        items = requisition.items.all()
        serializer = RequisitionItemSerializer(items, many=True)
        return Response({
            'requisition_number': requisition.requisition_number,
            'total_items': items.count(),
            'items': serializer.data
        })

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get all vendor assignments for a requisition"""
        requisition = self.get_object()
        assignments = VendorRequisitionAssignment.objects.filter(
            requisition=requisition
        ).select_related('vendor', 'assigned_by').prefetch_related('items')
        serializer = VendorRequisitionAssignmentSerializer(assignments, many=True)
        return Response({
            'requisition_number': requisition.requisition_number,
            'total_assignments': assignments.count(),
            'assignments': serializer.data
        })


class VendorAssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Vendor Assignment CRUD

    list: Get all vendor assignments
    create: Assign vendor to requisition items
    retrieve: Get assignment by ID
    destroy: Delete assignment (NOT ALLOWED)
    """
    queryset = VendorRequisitionAssignment.objects.all().select_related(
        'requisition', 'vendor', 'assigned_by'
    ).prefetch_related('items__product')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['requisition', 'vendor', 'assignment_date']
    search_fields = ['requisition__requisition_number', 'vendor__vendor_name']
    ordering_fields = ['assignment_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return VendorAssignmentCreateSerializer
        return VendorRequisitionAssignmentSerializer

    def perform_create(self, serializer):
        """Automatically set assigned_by to logged-in user"""
        serializer.save(assigned_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Prevent deletion of vendor assignments"""
        return Response(
            {
                'error': 'Vendor assignments cannot be deleted',
                'message': 'Assignments are permanent for audit trail'
            },
            status=status.HTTP_403_FORBIDDEN
        )

