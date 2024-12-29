from rest_framework import viewsets, status
from django.db.models import QuerySet
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, OR

from .serializers import BuySerializer, SellSerializer
from .swagger.swagger_serializers import SwaggerBuySerializer, SwaggerSellSerializer

from .models import Buy, Sell


class OperationsBaseViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'delete', 'put']
    # permission_classes = [OR(IsAdminUser, IsAuthenticatedOrReadOnly)]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        
        queryset = self.queryset.filter(wallet__user=user)
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
    
