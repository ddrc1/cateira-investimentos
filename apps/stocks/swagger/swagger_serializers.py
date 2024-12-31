from rest_framework import serializers

from ..models import Dividend, Stock, StockPrice, StockType


class SwaggerStockSerializer(serializers.ModelSerializer):
    stock_type = serializers.CharField()
    has_dividends = serializers.BooleanField()

    class Meta:
        model = Stock
        fields = ['id', 'code', 'description', 'stock_type', 'has_dividends']


class SwaggerStockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockType
        fields = ['id', 'type', 'description']


class SwaggerStockPriceSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()

    class Meta:
        model = StockPrice
        fields = ['id', 'stock', 'min_price', 'max_price', 'date']


class SwaggerDividendSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()
    
    class Meta:
        model = Dividend
        fields = ['id', 'stock', 'value', 'date']
