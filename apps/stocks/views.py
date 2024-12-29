from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from .permissions import ReadOnlyPermission

from .serializers import StockSerializer, StockTypeSerializer, StockPriceSerializer, DividendsSerializer
from .swagger.swagger_serializers import SwaggerStockSerializer, SwaggerStockTypeSerializer, SwaggerStockPriceSerializer, \
    SwaggerDividendsSerializer

from .models import StockType, Stock, StockPrice, Dividends


class StocksBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'put']
    permission_classes = [IsAdminUser | ReadOnlyPermission]

    def get_queryset(self):
        user = self.request.user
        print(user)
        return self.queryset
    
    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


class StockTypeViewSet(StocksBaseViewSet):
    queryset = StockType.objects.filter(active=True)
    serializer_class = StockTypeSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerStockTypeSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerStockTypeSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class StockViewSet(StocksBaseViewSet):
    queryset = Stock.objects.filter(active=True)
    serializer_class = StockSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerStockSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerStockSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class StockPriceViewSet(StocksBaseViewSet):
    queryset = StockPrice.objects.all()
    http_method_names = ['post', 'get', 'put']
    serializer_class = StockPriceSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerStockPriceSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerStockPriceSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class DividendsViewSet(StocksBaseViewSet):
    queryset = Dividends.objects.all()
    http_method_names = ['post', 'get', 'put']
    serializer_class = DividendsSerializer

    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerDividendsSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerDividendsSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)