from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer, \
    VendorPerformanceMetricSerializer
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from rest_framework.generics import RetrieveAPIView

class VendorViewSet(ModelViewSet):
    """
    This api will provide all crud operations on Vendor models.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'id'


class PurchaseOrderViewSet(ModelViewSet):
    """
    This api will provide all crud operations on PurchaseOrder models.
    """
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'id'
    

class HistoricalPerformanceViewSet(ReadOnlyModelViewSet):
    """
    This api will allow only get and retrieve api calls, No crud operations.
    """
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer


class RetrieveVendorPerformance(RetrieveAPIView):
    """
    This api will provide all crud operations on PurchaseOrder models.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceMetricSerializer
    lookup_field = 'id'
