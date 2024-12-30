from rest_framework import viewsets, views, status, exceptions
from rest_framework.response import Response
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema

from .serializers import BuySerializer, SellSerializer, CustodySerializer
from .swagger.swagger_serializers import SwaggerBuySerializer, SwaggerSellSerializer

from .models import Buy, Sell, Custody

class OperationsBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'put']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        
        queryset = self.queryset.filter(user=user)
        return queryset
    
    def perform_destroy(self, instance):
        instance.active = False
        instance.save()

class BuyViewSet(OperationsBaseViewSet):
    queryset = Buy.objects.filter(active=True)
    serializer_class = BuySerializer
    
    def get_queryset(self) -> QuerySet[Buy]:
        return super().get_queryset()
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerBuySerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerBuySerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class SellViewSet(OperationsBaseViewSet):
    queryset = Sell.objects.filter(active=True)
    serializer_class = SellSerializer

    def get_queryset(self) -> QuerySet[Sell]:
        return super().get_queryset()
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerSellSerializer()})
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(responses={status.HTTP_200_OK: SwaggerSellSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class CustodyViewSet(viewsets.ModelViewSet):
    queryset = Custody.objects.all()
    serializer_class = CustodySerializer
    http_method_names = ['get']

    def get_queryset(self) -> QuerySet[Custody]:
        return self.queryset.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)