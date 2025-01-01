from rest_framework import serializers

from ...operations.models import Buy, Sell
from ..serializers import CustodySerializer, CustodyDividendSerializer

class PaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()


class BuyResponseSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()
    user = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        model = Buy
        fields = ['id', 'volume', 'stock', 'price', 'total', 'date', 'user']


class SellResponseSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()
    user = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        model = Sell
        fields = ['id', 'volume', 'stock', 'price', 'total', 'date', 'user']


class PaginatedBuyResponseSerializer(PaginatedResponseSerializer):
    results = BuyResponseSerializer(many=True)

    
class PaginatedSellResponseSerializer(PaginatedResponseSerializer):
    results = BuyResponseSerializer(many=True)


class PaginatedCustodyResponseSerializer(PaginatedResponseSerializer):
    results = CustodySerializer(many=True)


class PaginatedCustodyDividendResponseSerializer(PaginatedResponseSerializer):
    results = CustodyDividendSerializer(many=True)
