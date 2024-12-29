from rest_framework import serializers

from ...operations.models import Buy, Sell

class SwaggerBuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = ['id', 'volume', 'stock', 'price', 'date', 'user']


class SwaggerSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = ['id', 'volume', 'stock', 'price', 'date', 'user']