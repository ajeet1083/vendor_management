from rest_framework import serializers
from vendor_app.models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
        
        
        
class VendorPerformanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformanceRecord
        fields = '__all__'
        
        
        
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        
        
        
class PurchaseOrderAcknowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        
        

