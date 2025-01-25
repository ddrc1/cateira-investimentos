from django.contrib import admin
from .models import Asset, AssetPrice, AssetType, Sector, SubSector, Dividend


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 20


class AdminAsset(BaseAdmin):
    list_display = ('id', 'code', 'full_name', 'description', 'sub_sector', 'asset_type', 'country', 'has_dividends', 'created_at', 'updated_at', 'active')
    list_filter = ('sub_sector', 'asset_type', 'country', 'updated_at', 'created_at', 'active')
    list_editable = ('code', 'full_name', 'description', 'sub_sector', 'asset_type', 'country', 'active')
    search_fields = ['code']


class AdminAssetPrice(BaseAdmin):
    list_display = ('id', 'asset', 'open_price', 'high_price', 'low_price', 'close_price', 'date')
    list_filter = ('date',)
    list_editable = ('open_price', 'high_price', 'low_price', 'close_price')


class AdminAssetTypePrice(BaseAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at', 'active')
    list_filter = ('created_at', 'updated_at', 'active')
    list_editable = ('name', 'description', 'active')


class AdminSector(BaseAdmin):
    list_display = ('id', 'name', 'description', 'created_at', 'updated_at', 'active')
    list_filter = ('created_at', 'updated_at', 'active')
    list_editable = ('name', 'description', 'active')

class AdminSubSector(BaseAdmin):
    list_display = ('id', 'name', 'description', 'sector', 'created_at', 'updated_at', 'active')
    list_filter = ('sector', 'created_at', 'updated_at', 'active')
    list_editable = ('name', 'description', 'sector', 'active')


class AdminDividend(BaseAdmin):
    list_display = ('id', 'asset', 'value', 'date')
    list_filter = ('date',)
    list_editable = ('asset', 'value')


admin.site.register(Asset, AdminAsset)
admin.site.register(AssetPrice, AdminAssetPrice)
admin.site.register(AssetType, AdminAssetTypePrice)
admin.site.register(Sector, AdminSector)
admin.site.register(SubSector, AdminSubSector)
admin.site.register(Dividend, AdminDividend)
