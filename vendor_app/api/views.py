from vendor_app.models import Vendor, PurchaseOrder, VendorPerformanceRecord
from vendor_app.api.serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceRecordSerializer, PurchaseOrderAcknowledgeSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone  
from django.db.models import Avg

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    
class PurchaseOrderVeiwSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
        
class PurchaseOrderAcknowledgeVeiwSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderAcknowledgeSerializer
    
    @action(detail=True, methods=['POST'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()

        # Check if the purchase order is in 'completed' status
        if purchase_order.status != 'completed':
            return Response({'error': 'Purchase Order is not in completed status'}, status=400)

        # Check if acknowledgment_date is already set
        if purchase_order.acknowledgment_date:
            return Response({'error': 'Acknowledgment already updated for this Purchase Order'}, status=400)

        # Trigger the acknowledgment logic
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Get the related vendor performance record
        vendor_performance_record = VendorPerformanceRecord.objects.filter(vendor=purchase_order.vendor).order_by('-date').first()

        # Trigger the recalculation of average_response_time
        vendor_performance_record.update_average_response_time()

        # Return a success response
        return Response({'success': 'Acknowledgment updated successfully'})
    
    
class VendorPerformanceRecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VendorPerformanceRecord.objects.all()
    serializer_class = VendorPerformanceRecordSerializer
    @action(detail=True, methods=['GET'])
    def performance(self, request, pk=None):
        # Get the vendor's performance records
        queryset = self.get_queryset().filter(vendor__id=pk)

        # Calculate the average values for each metric
        avg_on_time_delivery_rate = queryset.aggregate(Avg('on_time_delivery_rate'))['on_time_delivery_rate__avg']
        avg_quality_rating_avg = queryset.aggregate(Avg('quality_rating_avg'))['quality_rating_avg__avg']
        avg_average_response_time = queryset.aggregate(Avg('average_response_time'))['average_response_time__avg']
        avg_fulfillment_rate = queryset.aggregate(Avg('fulfillment_rate'))['fulfillment_rate__avg']

        # Create a dictionary with the calculated averages
        performance_data = {
            'on_time_delivery_rate': avg_on_time_delivery_rate,
            'quality_rating_avg': avg_quality_rating_avg,
            'average_response_time': avg_average_response_time,
            'fulfillment_rate': avg_fulfillment_rate,
        }

        return Response(performance_data)