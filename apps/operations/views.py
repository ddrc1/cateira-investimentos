from typing import Any
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema

from ..utils.pagination import CustomPageNumberPagination

from .serializers import BuySerializer, SellSerializer, CustodySerializer, CustodyDividendSerializer
from .swagger.swagger_serializers import BuyResponseSerializer, PaginatedBuyResponseSerializer, \
    SellResponseSerializer, PaginatedSellResponseSerializer, PaginatedCustodyResponseSerializer, \
    PaginatedCustodyDividendResponseSerializer

from .models import Buy, Sell, Custody, CustodyDividend
from ..authentication.models import User

class OperationsBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'put']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self) -> QuerySet[Any]:
        user: User = self.request.user
        if user.is_staff:
            return self.queryset
        
        queryset: QuerySet[Any] = self.queryset.filter(user=user)
        return queryset
    
    def perform_destroy(self, instance):
        instance.active = False
        instance.save()


class BuyViewSet(OperationsBaseViewSet):
    queryset = Buy.objects.filter(active=True)
    serializer_class = BuySerializer
        
    @swagger_auto_schema(responses={status.HTTP_200_OK: BuyResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedBuyResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: BuyResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: BuyResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    

class SellViewSet(OperationsBaseViewSet):
    queryset = Sell.objects.filter(active=True)
    serializer_class = SellSerializer
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SellResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedSellResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: SellResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SellResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class CustodyViewSet(viewsets.ModelViewSet):
    queryset = Custody.objects.all()
    serializer_class = CustodySerializer
    http_method_names = ['get']
    pagination_class = CustomPageNumberPagination

    serializers = {
        "default": serializer_class,
        "list_dividends": CustodyDividendSerializer,
        "retrieve_dividends": CustodyDividendSerializer
    }

    def get_serializer_class(self) -> Any:
        if self.action in self.serializers:
            return self.serializers[self.action]
        return self.serializers['default']
        
    def get_queryset(self) -> QuerySet[Custody | CustodyDividend]:
        queryset: QuerySet[Custody] = self.queryset.filter(user=self.request.user)

        if self.action in ["list_dividends", "retrieve_dividends"]:
            queryset: QuerySet[CustodyDividend] = CustodyDividend.objects.filter(custody__pk__in=queryset.values("pk"))

        return queryset
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedCustodyResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedCustodyDividendResponseSerializer()})
    @action(detail=False, methods=['get'], url_path="dividends")
    def list_dividends(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path="dividends/(?P<wallet_dividend_id>\d+)")
    def retrieve_dividends(self, request, *args, **kwargs):
        self.kwargs['pk'] = kwargs['wallet_dividend_id']
        return super().retrieve(request, *args, **kwargs)
