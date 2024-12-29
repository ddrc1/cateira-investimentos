from rest_framework.routers import DefaultRouter
from .views import BuyViewSet, SellViewSet

router = DefaultRouter()
router.register(r'buy', BuyViewSet, basename='buy')
router.register(r'sell', SellViewSet, basename='sell')

urlpatterns = router.urls