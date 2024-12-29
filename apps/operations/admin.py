from django.contrib import admin
from .models import Buy, Sell

class AdminBuy(admin.ModelAdmin):
    list_display = ('id', 'volume', 'stock', 'price', 'date', 'wallet', 'created_at', 'updated_at', 'active')
    list_filter = ('volume', 'stock', 'price', 'date', 'created_at', 'updated_at', 'wallet', 'active')
    list_editable = ('volume', 'stock', 'price', 'date', 'wallet', 'active')


class AdminSell(admin.ModelAdmin):
    list_display = ('id', 'volume', 'stock', 'price', 'date', 'wallet', 'created_at', 'updated_at', 'active')
    list_filter = ('volume', 'stock', 'price', 'date', 'created_at', 'updated_at', 'wallet', 'active')
    list_editable = ('volume', 'stock', 'price', 'date', 'wallet', 'active')


admin.site.register(Buy, AdminBuy)
admin.site.register(Sell, AdminSell)
