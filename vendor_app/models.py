from django.db import models
from django.db.models import JSONField, Count, Avg, F
from django.utils import timezone

# Create your models here.


# creating Vendor model for api
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.name
    


#creating PurchaseOrder model for api
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"
    
#  Creating VendorPerformanceRecord for api   
class VendorPerformanceRecord(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Performance Record for {self.vendor.name} on {self.date}"

    def update_on_time_delivery_rate(self):
        completed_pos = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            delivery_date__lte=self.date
        ).count()

        total_completed_pos = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed'
        ).count()

        if total_completed_pos > 0:
            self.on_time_delivery_rate = completed_pos / total_completed_pos
            self.save()

    def update_quality_rating_avg(self):
        completed_pos_with_ratings = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            quality_rating__isnull=False
        )

        avg_quality_rating = completed_pos_with_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg']

        if avg_quality_rating is not None:
            self.quality_rating_avg = avg_quality_rating
            self.save()

    def update_average_response_time(self):
        acknowledged_pos = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            acknowledgment_date__isnull=False
        )

        avg_response_time = acknowledged_pos.aggregate(
            avg_response_time=Avg(F('acknowledgment_date') - F('issue_date'))
        )['avg_response_time']

        if avg_response_time is not None:
            self.average_response_time = avg_response_time.total_seconds()
            self.save()

    def update_fulfillment_rate(self):
        successful_pos = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            issues__isnull=True
        ).count()

        total_pos = PurchaseOrder.objects.filter(
            vendor=self.vendor
        ).count()

        if total_pos > 0:
            self.fulfillment_rate = successful_pos / total_pos
            self.save()