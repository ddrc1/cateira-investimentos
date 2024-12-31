from rest_framework import serializers

from .models import Dividend, Stock, StockType, StockPrice


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "code": instance.code,
            "description": instance.description,
            "stock_type": instance.stock_type.type,
            "has_dividends": instance.has_dividends
        }

        return representation


class StockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockType
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "type": instance.type,
            "description": instance.description
        }

        return representation

class StockPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockPrice
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "stock": instance.stock.code,
            "min_price": instance.min_price,
            "mean_price": instance.mean_price,
            "max_price": instance.max_price,
            "date": instance.date,
        }

        return representation
    

class DividendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dividend
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "stock": instance.stock.code,
            "value": instance.min_price,
            "date": instance.date,
        }

        return representation