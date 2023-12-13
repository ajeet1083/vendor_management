from django.urls import path, include
from vendor_app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('vendors', views.VendorViewSet, basename='vendor')
router.register('purchase_orders', views.PurchaseOrderVeiwSet, basename='purchase_orders')
router.register('vendors', views.VendorPerformanceRecordViewSet, basename='vendor-performance')
router.register('purchase_orders', views.PurchaseOrderAcknowledgeVeiwSet, basename='vendor-performance')



urlpatterns = [
   path('', include(router.urls)),
  ]
