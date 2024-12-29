from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockPriceViewSet, StockTypeViewSet, StockViewSet

router = DefaultRouter()
router.register(r'price', StockPriceViewSet, basename='stock-price')
router.register(r'type', StockTypeViewSet, basename='stock-type')
router.register(r'stock', StockViewSet, basename='stock')

urlpatterns = router.urls