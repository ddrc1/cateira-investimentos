from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from .permissions import ReadOnlyPermission
from ..utils.pagination import CustomPageNumberPagination

from .serializers import AssetSerializer, AssetTypeSerializer, SectorSerializer, SubSectorSerializer, AssetPriceSerializer, DividendSerializer
from .swagger.swagger_serializers import AssetResponseSerializer, AssetTypeResponseSerializer, AssetPriceResponseSerializer, \
    DividendResponseSerializer, PaginatedAssetResponseSerializer, PaginatedAssetTypeResponseSerializer, SubSectorResponseSerializer, \
    SectorResponseSerializer, PaginatedAssetPriceResponseSerializer, PaginatedDividendResponseSerializer, PaginatedSubSectorResponseSerializer, \
    PaginatedSectorResponseSerializer

from .models import AssetType, Asset, SubSector, Sector, AssetPrice, Dividend

from ..cron.cron import get_ticker_price_data


class AssetsBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'put']
    permission_classes = [IsAdminUser | ReadOnlyPermission]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset.order_by('pk')
    
    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


class AssetTypeViewSet(AssetsBaseViewSet):
    queryset = AssetType.objects.filter(active=True)
    serializer_class = AssetTypeSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: AssetTypeResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedAssetTypeResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: AssetTypeResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: AssetTypeResponseSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class SubSectorViewSet(AssetsBaseViewSet):
    queryset = SubSector.objects.filter(active=True)
    serializer_class = SubSectorSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SubSectorResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedSubSectorResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: SubSectorResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SubSectorResponseSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class SectorViewSet(AssetsBaseViewSet):
    queryset = Sector.objects.filter(active=True)
    serializer_class = SectorSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SectorResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedSectorResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: SectorResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SectorResponseSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AssetViewSet(AssetsBaseViewSet):
    queryset = Asset.objects.filter(active=True)
    serializer_class = AssetSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: AssetResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedAssetResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: AssetResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: AssetResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class AssetPriceViewSet(AssetsBaseViewSet):
    queryset = AssetPrice.objects.all()
    http_method_names = ['post', 'get', 'put']
    serializer_class = AssetPriceSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: AssetPriceResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedAssetPriceResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: AssetPriceResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: AssetPriceResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class DividendViewSet(AssetsBaseViewSet):
    queryset = Dividend.objects.all()
    http_method_names = ['post', 'get', 'put']
    serializer_class = DividendSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: DividendResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedDividendResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: DividendResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: DividendResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)