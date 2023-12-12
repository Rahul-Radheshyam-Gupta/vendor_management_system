# models.py
from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator

class PerformanceBaseModel(models.Model):
    on_time_delivery_rate = models.FloatField(default=None, null=True)
    quality_rating_avg = models.FloatField(default=None, null=True)
    average_response_time = models.DurationField(default=None, null=True) # for Sqlite - stored in microsecs
    fulfillment_rate = models.FloatField(default=None, null=True)

    class Meta:
        abstract = True

class Vendor(PerformanceBaseModel):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Vendor - {self.name}"


STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'),
]

class PurchaseOrder(models.Model):
    po_number = models.CharField(default=uuid4, max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True) # when PO is created
    delivery_date = models.DateTimeField(default=None, null=True, blank=True) # Expected Delivery Date
    items = models.JSONField(null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    quality_rating = models.FloatField(default=None, null=True, blank=True, validators=[MaxValueValidator(5)])
    issue_date = models.DateTimeField(default=None, null=True, blank=True) # when status = Completed
    acknowledgment_date = models.DateTimeField(default=None, null=True, blank=True) # when vendor ack that he has received

    def __str__(self):
        return f"PO-{self.po_number} for {self.vendor.name}"

class HistoricalPerformance(PerformanceBaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.vendor.name} - {self.date.strftime('%Y-%m-%d')}"
