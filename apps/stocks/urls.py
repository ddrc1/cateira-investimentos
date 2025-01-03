from rest_framework.routers import DefaultRouter
from .views import StockPriceViewSet, StockTypeViewSet, StockViewSet, DividendViewSet, StockSubTypeViewSet

router = DefaultRouter()
router.register(r'price', StockPriceViewSet, basename='stock-price')
router.register(r'type', StockTypeViewSet, basename='stock-type')
router.register(r'sub-type', StockSubTypeViewSet, basename='stock-sub-type')
router.register(r'dividend', DividendViewSet, basename='dividend')
router.register(r'', StockViewSet, basename='stock')

urlpatterns = router.urls