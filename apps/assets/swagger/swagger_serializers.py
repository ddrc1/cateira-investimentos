from rest_framework import serializers

from ..models import Dividend, Asset, AssetPrice, Sector, SubSector, AssetType


class PaginatedResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    next = serializers.URLField()
    previous = serializers.URLField()


class AssetResponseSerializer(serializers.ModelSerializer):
    sub_sector = serializers.CharField()
    has_dividends = serializers.BooleanField()

    class Meta:
        model = Asset
        fields = ['id', 'code', 'description', 'sub_sector', 'has_dividends']


class AssetTypeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ['id', 'name', 'description']


class SectorResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['id', 'name', 'description']


class SubSectorResponseSerializer(serializers.ModelSerializer):
    sector = serializers.CharField()

    class Meta:
        model = SubSector
        fields = ['id', 'name', 'sector', 'description']


class AssetPriceResponseSerializer(serializers.ModelSerializer):
    asset = serializers.CharField()

    class Meta:
        model = AssetPrice
        fields = ['id', 'asset', 'open_price', 'high_price', 'low_price', 'close_price', 'date']


class DividendResponseSerializer(serializers.ModelSerializer):
    asset = serializers.CharField()
    
    class Meta:
        model = Dividend
        fields = ['id', 'asset', 'value', 'date']


class PaginatedAssetResponseSerializer(PaginatedResponseSerializer):
    results = AssetResponseSerializer(many=True)


class PaginatedAssetTypeResponseSerializer(PaginatedResponseSerializer):
    results = AssetTypeResponseSerializer(many=True)


class PaginatedAssetPriceResponseSerializer(PaginatedResponseSerializer):
    results = AssetPriceResponseSerializer(many=True)


class PaginatedDividendResponseSerializer(PaginatedResponseSerializer):
    results = DividendResponseSerializer(many=True)


class PaginatedSectorResponseSerializer(PaginatedResponseSerializer):
    results = SectorResponseSerializer(many=True)


class PaginatedSubSectorResponseSerializer(PaginatedResponseSerializer):
    results = SubSectorResponseSerializer(many=True)