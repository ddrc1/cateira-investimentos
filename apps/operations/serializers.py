from rest_framework import serializers

from .models import Buy, Sell


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'volume': instance.volume,
            'stock': instance.stock.code,
            'price': instance.price,
            'date': instance.date,
            'user': instance.user.email
        }

        return representation


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'volume': instance.volume,
            'stock': instance.stock.code,
            'price': instance.price,
            'date': instance.date,
            'user': instance.user.email
        }

        return representation