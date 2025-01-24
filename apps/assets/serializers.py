from rest_framework import serializers

from .models import Dividend, Asset, AssetType, AssetPrice, Sector, SubSector


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "code": instance.code,
            "full_name": instance.full_name,
            "description": instance.description,
            "sub_sector": instance.sub_sector.name if instance.sub_sector else None,
            "asset_type": instance.asset_type.name,
            "has_dividends": instance.has_dividends
        }

        return representation


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "name": instance.name,
            "description": instance.description
        }

        return representation
    

class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "name": instance.name,
            "description": instance.description
        }

        return representation
    

class SubSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSector
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "name": instance.name,
            "description": instance.description,
            "sector": instance.sector.name
        }

        return representation
    

class AssetPriceSerializer(serializers.ModelSerializer):
    open_price = serializers.FloatField(min_value=0)
    high_price = serializers.FloatField(min_value=0)
    low_price = serializers.FloatField(min_value=0)
    close_price = serializers.FloatField(min_value=0)

    class Meta:
        model = AssetPrice
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "asset": instance.asset.code,
            "open_price": instance.open_price,
            "high_price": instance.high_price,
            "low_price": instance.low_price,
            "close_price": instance.close_price,
            "date": instance.date,
        }

        return representation
    

class DividendSerializer(serializers.ModelSerializer):
    value = serializers.FloatField(min_value=0)
    
    class Meta:
        model = Dividend
        fields = '__all__'

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "asset": instance.asset.code,
            "value": instance.min_price,
            "date": instance.date,
        }

        return representation