from rest_framework import serializers

from ..models import Dividend, Stock, StockPrice, StockType


class PaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()


class StockResponseSerializer(serializers.ModelSerializer):
    stock_type = serializers.CharField()
    has_dividends = serializers.BooleanField()

    class Meta:
        model = Stock
        fields = ['id', 'code', 'description', 'stock_type', 'has_dividends']


class StockTypeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockType
        fields = ['id', 'type', 'description']


class StockPriceResponseSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()

    class Meta:
        model = StockPrice
        fields = ['id', 'stock', 'min_price', 'max_price', 'date']


class DividendResponseSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()
    
    class Meta:
        model = Dividend
        fields = ['id', 'stock', 'value', 'date']


class PaginatedStockResponseSerializer(PaginatedResponseSerializer):
    results = StockResponseSerializer(many=True)


class PaginatedStockTypeResponseSerializer(PaginatedResponseSerializer):
    results = StockTypeResponseSerializer(many=True)


class PaginatedStockPriceResponseSerializer(PaginatedResponseSerializer):
    results = StockPriceResponseSerializer(many=True)


class PaginatedDividendResponseSerializer(PaginatedResponseSerializer):
    results = DividendResponseSerializer(many=True)