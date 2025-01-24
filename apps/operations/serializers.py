from rest_framework import serializers
from django.db import transaction
from drf_yasg.utils import swagger_serializer_method


from .models import Buy, Sell, Custody, CustodyDividend
from ..assets.models import Dividend, Asset
from ..authentication.models import User


class BuySerializer(serializers.ModelSerializer):
    value = serializers.FloatField(min_value=0)
    volume = serializers.FloatField(min_value=0)

    class Meta:
        model = Buy
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        buy = Buy.objects.create(**validated_data)
        custody, _ = Custody.objects.get_or_create(asset=validated_data['asset'], user=validated_data['user'])
        custody.rebuild()

        return buy
    
    @transaction.atomic
    def update(self, instance, validated_data):
        for key, value in validated_data.items:
            setattr(instance, key, value)

        instance.save()

        try:
            custody = Custody.objects.get(asset=validated_data['asset'], user=validated_data['user'])
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
            'asset': instance.asset.code,
            'price': instance.price,
            'date': instance.date,
            'user': instance.user.username
        }

        return representation


class SellSerializer(serializers.ModelSerializer):
    value = serializers.FloatField(min_value=0)
    volume = serializers.FloatField(min_value=0)

    class Meta:
        model = Sell
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        sell = Sell.objects.create(**validated_data)
        try:
            custody = Custody.objects.get(asset=validated_data['asset'], user=validated_data['user'])
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
            custody = Custody.objects.get(asset=validated_data['asset'], user=validated_data['user'])
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
            'asset': instance.asset.code,
            'price': instance.price,
            'date': instance.date,
            'user': instance.user.username
        }

        return representation


class CustodySerializer(serializers.ModelSerializer):
    last_price = serializers.FloatField()
    mean_price = serializers.FloatField()
    total_value = serializers.FloatField()
    balance = serializers.FloatField()
    asset = serializers.SlugRelatedField(queryset=Asset.objects.filter(active=True), slug_field='code')
    user = serializers.SlugRelatedField(queryset=User.objects.filter(active=True), slug_field='username')
    dividend_amount_received = serializers.FloatField()

    class Meta:
        model = Custody
        exclude = ['created_at', 'updated_at', 'active']
        

class CustodyDividendSerializer(serializers.ModelSerializer):
    volume = serializers.FloatField(min_value=0)

    class Meta:
        model = CustodyDividend
        fields = '__all__'

    def validate(self, attrs):
        if attrs['custody'].asset != attrs['dividend'].asset:
            raise serializers.ValidationError("The custody and dividend must be from the same asset")
        
        return attrs

    def to_representation(self, instance):
        representation = {
            'id': instance.id,
            'asset': instance.custody.asset.code,
            'volume': instance.volume,
            'value': instance.dividend.value,
            'amount_received': instance.amount_received,
            'date': instance.dividend.date
        }

        return representation
    