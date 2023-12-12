from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .helper import (
    get_fulfillment_rate, get_average_response_time, get_quality_rating_avg, get_on_time_delivery_rate, audit_vendor_performance
)
from django.utils import timezone

@receiver(pre_save, sender=PurchaseOrder)
def validate_and_set_default(sender, instance, **kwargs):
    if instance.status == 'Completed'and not instance.issue_date:
        instance.issue_date = timezone.now()
    return instance



@receiver(post_save, sender=PurchaseOrder)
def update_vendor_stats(sender, instance, created, **kwargs):
    print(f"In post save of Purchase Order - {created} - {instance.status}")
    vendor = instance.vendor
    if instance.status == 'Completed':
        vendor = get_on_time_delivery_rate(vendor, instance)
        vendor = get_quality_rating_avg(vendor, instance)
        vendor = get_average_response_time(vendor, instance)
    vendor = get_fulfillment_rate(vendor, instance)
    vendor.save()
    audit_vendor_performance(vendor)