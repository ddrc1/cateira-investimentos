from rest_framework import serializers

from .models import Dividends, Stock, StockType, StockPrice


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "code": instance.code,
            "description": instance.description,
            "stock_type": instance.stock_type.type
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
            "max_price": instance.max_price,
            "date": instance.date,
        }

        return representation
    

class DividendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dividends
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "stock": instance.stock.code,
            "value": instance.min_price,
            "date": instance.date,
        }

        return representation