from rest_framework import serializers
from django.db import transaction
from drf_yasg.utils import swagger_serializer_method


from .models import Buy, Sell, Custody, CustodyDividend
from ..stocks.models import Dividend, Stock
from ..authentication.models import User


class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buy
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        buy = Buy.objects.create(**validated_data)
        try:
            custody = Custody.objects.get(stock=validated_data['stock'], user=validated_data['user'])
        except Custody.DoesNotExist:
            custody = Custody.objects.create(stock=validated_data['stock'], user=validated_data['user'])
            custody.save()
        
        custody.rebuild()

        return buy
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items:
            setattr(instance, key, value)

        instance.save()

        try:
            custody = Custody.objects.get(stock=validated_data['stock'], user=validated_data['user'])
            try:
                custody.rebuild()
            except ValueError as e:
                raise serializers.ValidationError(e.args)
        except Custody.DoesNotExist:
            raise serializers.ValidationError("Couldn't find the wallet")

        return instance

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'volume': instance.volume,
            'stock': instance.stock.code,
            'price': instance.price,
            'date': instance.date,
            'user': instance.user.username
        }

        return representation


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sell
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        sell = Sell.objects.create(**validated_data)
        try:
            custody = Custody.objects.get(stock=validated_data['stock'], user=validated_data['user'])
            custody.rebuild()
        except Custody.DoesNotExist:
            raise serializers.ValidationError("Couldn't find the wallet")
        
        return sell
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items:
            setattr(instance, key, value)

        instance.save()

        try:
            custody = Custody.objects.get(stock=validated_data['stock'], user=validated_data['user'])
            try:
                custody.rebuild()
            except ValueError as e:
                raise serializers.ValidationError(e.args)
        except Custody.DoesNotExist:
            raise serializers.ValidationError("Couldn't find the wallet")

        return instance

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'volume': instance.volume,
            'stock': instance.stock.code,
            'price': instance.price,
            'date': instance.date,
            'user': instance.user.username
        }

        return representation


class CustodySerializer(serializers.ModelSerializer):
    current_price = serializers.FloatField()
    mean_price = serializers.FloatField()
    total_value = serializers.FloatField()
    balance = serializers.FloatField()
    stock = serializers.SlugRelatedField(queryset=Stock.objects.filter(active=True), slug_field='code')
    user = serializers.SlugRelatedField(queryset=User.objects.filter(active=True), slug_field='username')
    dividend_amount_received = serializers.FloatField()

    class Meta:
        model = Custody
        exclude = ['created_at', 'updated_at', 'active']
        

class CustodyDividendSerializer(serializers.ModelSerializer):
    stock = serializers.SlugRelatedField(queryset=Dividend.objects.all(), slug_field='code', source='dividend.stock')
    user = serializers.SlugRelatedField(queryset=Custody.objects.all(), slug_field='username', source='custody.user')
    amount_received = serializers.FloatField()
    date = serializers.SerializerMethodField()
    
    class Meta:
        model = CustodyDividend
        exclude = ["custody", "dividend"]

    @swagger_serializer_method(serializers.DateField())
    def get_date(self, obj):
        return  obj.dividend.date
    