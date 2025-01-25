from rest_framework import serializers

from ...operations.models import Buy, Sell
from ..serializers import CustodySerializer, CustodySnapshotSerializer

class PaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()


class BuyResponseSerializer(serializers.ModelSerializer):
    asset = serializers.CharField()
    user = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        model = Buy
        fields = ['id', 'volume', 'asset', 'price', 'total', 'date', 'user']


class SellResponseSerializer(serializers.ModelSerializer):
    asset = serializers.CharField()
    user = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        model = Sell
        fields = ['id', 'volume', 'asset', 'price', 'total', 'date', 'user']


class CustodyDividendResponseSerializer(serializers.ModelSerializer):
    asset = serializers.CharField()
    value = serializers.FloatField()
    amount_received = serializers.FloatField()
    date = serializers.DateField()

    class Meta:
        model = Sell
        fields = ['id', 'volume', 'asset', 'value', 'amount_received', 'date']


class PaginatedBuyResponseSerializer(PaginatedResponseSerializer):
    results = BuyResponseSerializer(many=True)

    
class PaginatedSellResponseSerializer(PaginatedResponseSerializer):
    results = BuyResponseSerializer(many=True)


class PaginatedCustodyResponseSerializer(PaginatedResponseSerializer):
    results = CustodySerializer(many=True)


class PaginatedCustodyDividendResponseSerializer(PaginatedResponseSerializer):
    results = CustodyDividendResponseSerializer(many=True)


class PaginatedCustodySnapshotResponseSerializer(PaginatedResponseSerializer):
    results = CustodySnapshotSerializer(many=True)
