from rest_framework import routers
from .apiviews import VendorViewSet, PurchaseOrderViewSet, HistoricalPerformanceViewSet, RetrieveVendorPerformance
from django.urls import path

router = routers.DefaultRouter()
router.register('vendors', VendorViewSet, basename='vendor')
router.register('purchase_order', PurchaseOrderViewSet, basename='po')
router.register('histories', HistoricalPerformanceViewSet, basename='history')

urlpatterns = router.urls
urlpatterns.append(
    path('vendors/<int:id>/performance/', RetrieveVendorPerformance.as_view(), name='vendor-performance')
)
