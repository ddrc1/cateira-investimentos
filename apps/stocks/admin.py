from django.contrib import admin
from .models import Stock, StockPrice, StockType, Dividend

class AdminStock(admin.ModelAdmin):
    list_display = ('id', 'code', 'description', 'stock_type', 'has_dividends', 'created_at', 'updated_at', 'active')
    list_filter = ('stock_type', 'updated_at', 'created_at', 'active')
    list_editable = ('code', 'description', 'stock_type', 'active')


class AdminStockPrice(admin.ModelAdmin):
    list_display = ('id', 'stock', 'min_price', 'max_price', 'date')
    list_filter = ('stock', 'date',)
    list_editable = ('stock', 'min_price', 'max_price')


class AdminStockTypePrice(admin.ModelAdmin):
    list_display = ('id', 'type', 'description', 'created_at', 'updated_at', 'active')
    list_filter = ('created_at', 'updated_at', 'active')
    list_editable = ('type', 'description', 'active')


class AdminDividend(admin.ModelAdmin):
    list_display = ('id', 'stock', 'value', 'date')
    list_filter = ('stock', 'date')
    list_editable = ('stock', 'value')


admin.site.register(Stock, AdminStock)
admin.site.register(StockPrice, AdminStockPrice)
admin.site.register(StockType, AdminStockTypePrice)
admin.site.register(Dividend, AdminDividend)
