from core.models import PurchaseOrder, HistoricalPerformance
from django.db.models import Count,IntegerField, FloatField, DurationField, ExpressionWrapper, Q, F, When, Case, Avg
from django.db.models.functions import Cast
from django.utils import timezone
def get_on_time_delivery_rate(vendor, instance):
    """
    ● Calculated each time a PO status changes to 'completed'.
    ● Logic: Count the number of completed POs delivered on or before delivery_date and divide by the total number of completed POs for that vendor.
    """
    on_time_delivery_rate_query = PurchaseOrder.objects.filter(vendor_id=vendor.id).aggregate(
        on_time_delivery_rate = Cast(
            Count(
                Case(
                    When(
                        Q(delivery_date__lte=timezone.now()) & Q(delivery_date__isnull=False),
                        then=1
                    ),
                    default=0.0,
                    output_field=FloatField()
                )
            ) / Count('id'),
            output_field=FloatField()
        )
    )
    vendor.on_time_delivery_rate = on_time_delivery_rate_query['on_time_delivery_rate']
    print(f"calculated delivery_rate", on_time_delivery_rate_query)
    return vendor

def get_quality_rating_avg(vendor, instance):
    """
    ● Updated upon the completion of each PO where a quality_rating is provided.
    ● Logic: Calculate the average of all quality_rating values for completed POs of the vendor.
    """
    if instance.status == 'Completed' and instance.quality_rating:
        quality_rating_query = PurchaseOrder.objects.filter(vendor_id=vendor.id, status='Completed').aggregate(
             quality_rating_avg = Avg('quality_rating')
        )
        vendor.quality_rating_avg = quality_rating_query['quality_rating_avg']
        print(f"calculated avg quality rating", quality_rating_query)
    return vendor

def get_average_response_time(vendor, instance):
    """
    ● Calculated each time a PO is acknowledged by the vendor.
    ● Logic: Compute the time difference between issue_date and acknowledgment_date for each PO, 
    and then find the average of these times for all POs of the vendor.
    """
    if instance.status == 'Completed' and instance.acknowledgment_date:
        average_response_time_query = PurchaseOrder.objects.filter(vendor_id=vendor.id, status='Completed').annotate(
            response_time = ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date')
            ,
            output_field=DurationField()
            )
        ).aggregate(
             average_response_time = Avg('response_time')
        )
        print(f"calculated avg response timing", average_response_time_query)
        vendor.average_response_time = average_response_time_query['average_response_time']
    return vendor

def get_fulfillment_rate(vendor, instance):
    """
    ● Calculated upon any change in PO status.
    ● Logic: Divide the number of successfully fulfilled POs (status 'completed' without issues) 
    by the total number of POs issued to the vendor.
    """
    fulfillment_rate_query = PurchaseOrder.objects.filter(vendor_id=vendor.id).aggregate(
        total_po=Count('id'),
        successful_po=Count(
            Case(
                When(
                    Q(status='Completed', quality_rating__isnull=True), then=1
                ),
                output_field=IntegerField()
            )
        )
    )
    total_po = fulfillment_rate_query['total_po']
    successful_po = fulfillment_rate_query['successful_po']
    print(f"calculated fulfillment rate", fulfillment_rate_query)
    vendor.fulfillment_rate = successful_po*100/total_po if total_po > 0 else 0
    return vendor


def audit_vendor_performance(vendor):
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )