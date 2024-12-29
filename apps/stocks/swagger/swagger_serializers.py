from rest_framework import serializers

from ..models import Dividends, Stock, StockPrice, StockType


class SwaggerStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'code', 'description', 'stock_type']


class SwaggerStockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockType
        fields = ['id', 'type', 'description']


class SwaggerStockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = ['id', 'stock', 'min_price', 'max_price', 'date']


class SwaggerDividendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dividends
        fields = ['id', 'stock', 'value', 'date']
