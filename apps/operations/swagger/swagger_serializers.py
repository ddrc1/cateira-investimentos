from rest_framework import serializers

from ...operations.models import Buy, Sell, Custody, CustodyDividend

class SwaggerBuySerializer(serializers.ModelSerializer):
    stock = serializers.CharField()
    user = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        model = Buy
        fields = ['id', 'volume', 'stock', 'price', 'total', 'date', 'user']


class SwaggerSellSerializer(serializers.ModelSerializer):
    stock = serializers.CharField()
    user = serializers.CharField()
    total = serializers.FloatField()

    class Meta:
        model = Sell
        fields = ['id', 'volume', 'stock', 'price', 'total', 'date', 'user']
