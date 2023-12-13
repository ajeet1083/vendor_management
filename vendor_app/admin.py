from django.contrib import admin
from vendor_app.models import *
# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vendor._meta.fields]
    

# register PurchageOrder Model
@admin.register(PurchaseOrder)
class PurchageOrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PurchaseOrder._meta.fields]


# register VendorPerformanceRecord Model
@admin.register(VendorPerformanceRecord)
class VendorPerformanceRecord(admin.ModelAdmin):
    list_display = [field.name for field in VendorPerformanceRecord._meta.fields]