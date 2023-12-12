from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='vendor-detail', lookup_field='id', read_only=True, format='html')
    class Meta:
        model = Vendor
        fields = ('id','url', 'name', 'contact_details', 'address', 'vendor_code')


class VendorPerformanceMetricSerializer(serializers.ModelSerializer):
    average_response_time = serializers.SerializerMethodField()

    def get_average_response_time(self, obj):
         """
         Return avg response time in the readable format
         """
         days = obj.average_response_time.days
         seconds = obj.average_response_time.seconds
         hours = seconds // 3600
         seconds = (seconds - hours*3600)//60
         res = ""
         if days:
             res += f"{days} days "
         if hours:
             res += f"{hours} hours "
         if seconds:
             res += f"{seconds} Mins"
         return res

    class Meta:
        model = Vendor
        fields = ('id', 'name', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')


class PurchaseOrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='po-detail', lookup_field='id', read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = '__all__'                              
        read_only_fields = ('po_number',)
        

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'


