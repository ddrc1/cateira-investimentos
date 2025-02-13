from rest_framework.routers import DefaultRouter
from .views import BuyViewSet, SellViewSet, CustodyViewSet, CustodyDividendViewSet, CustodySnapshotViewSet

router = DefaultRouter()
router.register(r'buy', BuyViewSet, basename='buy')
router.register(r'sell', SellViewSet, basename='sell')
router.register(r'wallet', CustodyViewSet, basename='wallet')
router.register(r'dividend', CustodyDividendViewSet, basename='wallet-dividend')
router.register(r'snapshot', CustodySnapshotViewSet, basename='snapshot')

urlpatterns = router.urls