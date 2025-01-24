from rest_framework.routers import DefaultRouter
from .views import AssetPriceViewSet, AssetTypeViewSet, AssetViewSet, DividendViewSet, SectorViewSet, SubSectorViewSet

router = DefaultRouter()
router.register(r'price', AssetPriceViewSet, basename='asset-price')
router.register(r'type', AssetTypeViewSet, basename='asset-type')
router.register(r'sector', SectorViewSet, basename='asset-sector')
router.register(r'sub-sector', SubSectorViewSet, basename='asset-sub-sector')
router.register(r'dividend', DividendViewSet, basename='dividend')
router.register(r'', AssetViewSet, basename='asset')

urlpatterns = router.urls