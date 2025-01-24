from typing import Any
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..utils.pagination import CustomPageNumberPagination

from .serializers import BuySerializer, SellSerializer, CustodySerializer, CustodyDividendSerializer
from .swagger.swagger_serializers import BuyResponseSerializer, PaginatedBuyResponseSerializer, \
    SellResponseSerializer, PaginatedSellResponseSerializer, PaginatedCustodyResponseSerializer, \
    PaginatedCustodyDividendResponseSerializer, CustodyDividendResponseSerializer

from .models import Buy, Sell, Custody, CustodyDividend
from ..authentication.models import User

class OperationsBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'put']
    pagination_class = CustomPageNumberPagination

    def get_queryset(self) -> QuerySet[Any]:
        user: User = self.request.user
        if not user.is_staff:
            queryset: QuerySet[Any] = self.queryset.filter(user=user)

        return queryset.order_by("pk")
    
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
        
    def get_queryset(self) -> QuerySet[Custody]:
        queryset: QuerySet[Custody] = self.queryset.filter(user=self.request.user)

        return queryset.order_by("pk")
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedCustodyResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: CustodyDividendResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class CustodyDividendViewSet(viewsets.ModelViewSet):
    queryset = CustodyDividend.objects.filter(active=True)
    http_method_names = ['get', 'put', 'post', 'delete']
    serializer_class = CustodyDividendSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self) -> QuerySet[CustodyDividend]:
        queryset: QuerySet[CustodyDividend] = self.queryset.filter(custody__user=self.request.user)
        return queryset.order_by("-dividend__date")

    def perform_destroy(self, instance):
        instance.active = False
        instance.save()

    @swagger_auto_schema(responses={status.HTTP_200_OK: PaginatedCustodyDividendResponseSerializer()})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(responses={status.HTTP_200_OK: CustodyDividendResponseSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_201_CREATED: CustodyDividendResponseSerializer()})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: CustodyDividendResponseSerializer()})
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)