from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from .permissions import ReadOnlyPermission
from ..utils.pagination import CustomPageNumberPagination

from .serializers import StockSerializer, StockTypeSerializer, StockSubTypeSerializer, StockPriceSerializer, DividendSerializer
from .swagger.swagger_serializers import StockResponseSerializer, StockTypeResponseSerializer, StockPriceResponseSerializer, \
    DividendResponseSerializer, PaginatedStockResponseSerializer, PaginatedStockTypeResponseSerializer, \
    PaginatedStockPriceResponseSerializer, PaginatedDividendResponseSerializer, StockSubTypeResponseSerializer, \
    PaginatedStockSubTypeResponseSerializer

from .models import StockType, Stock, StockPrice, Dividend


class StocksBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'put']
    permission_classes = [IsAdminUser | ReadOnlyPermission]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return self.queryset
    
    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


class StockTypeViewSet(StocksBaseViewSet):
    queryset = StockType.objects.filter(active=True)
    serializer_class = StockTypeSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: StockTypeResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedStockTypeResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: StockTypeResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: StockTypeResponseSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class StockSubTypeViewSet(StocksBaseViewSet):
    queryset = StockType.objects.filter(active=True)
    serializer_class = StockSubTypeSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: StockSubTypeResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedStockSubTypeResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: StockSubTypeResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: StockSubTypeResponseSerializer})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class StockViewSet(StocksBaseViewSet):
    queryset = Stock.objects.filter(active=True)
    serializer_class = StockSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: StockResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedStockResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: StockResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: StockResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class StockPriceViewSet(StocksBaseViewSet):
    queryset = StockPrice.objects.all()
    http_method_names = ['post', 'get', 'put']
    serializer_class = StockPriceSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: StockPriceResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedStockPriceResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: StockPriceResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: StockPriceResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class DividendViewSet(StocksBaseViewSet):
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