from django.contrib import admin
from django.db import transaction
from django.core import exceptions

from .models import Buy, Sell, Custody, CustodyDividend

class AdminBuy(admin.ModelAdmin):
    list_display = ('id', 'asset', 'volume', 'price', 'date', 'user', 'created_at', 'updated_at', 'active')
    list_filter = ('asset', 'date', 'created_at', 'updated_at', 'user', 'active')
    list_editable = ('volume', 'asset', 'price', 'date', 'user', 'active')

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            custody = Custody.objects.get(user=obj.user, asset=obj.asset)
        except Custody.DoesNotExist:
            if change:
                raise exceptions.ObjectDoesNotExist("Custody object does not exist")
            else:
                custody = Custody.objects.create(asset=obj.asset, user=obj.user)
                custody.save()
        
        try:
            custody.rebuild()
        except Exception as e:
            raise exceptions.ValidationError(e.args)
        


class AdminSell(admin.ModelAdmin):
    list_display = ('id', 'asset', 'volume', 'price', 'date', 'user', 'created_at', 'updated_at', 'active')
    list_filter = ('asset', 'date', 'created_at', 'updated_at', 'user', 'active')
    list_editable = ('volume', 'asset', 'price', 'date', 'user', 'active')

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            custody = Custody.objects.get(user=obj.user, asset=obj.asset)
            custody.rebuild()
        except Custody.DoesNotExist:
            raise exceptions.ObjectDoesNotExist("Custody object does not exist")
        except Exception as e:
            raise exceptions.ValidationError(e.args)


class AdminCostody(admin.ModelAdmin):
    list_display = ('id', 'asset', 'volume', 'total_cost', 'last_price', 'mean_price', 'total_value', 'balance', 
                    'user', 'created_at', 'updated_at', 'active')
    list_filter = ('created_at', 'updated_at', 'active')


class AdminCostodyDividend(admin.ModelAdmin):
    list_display = ('id', 'custody__asset', 'volume', 'dividend__value', 'amount_received', 'custody__user', 'dividend__date')
    list_filter = ('dividend__date', 'created_at', 'updated_at', 'active')
    list_editable = ('volume',)


admin.site.register(Buy, AdminBuy)
admin.site.register(Sell, AdminSell)
admin.site.register(Custody, AdminCostody)
admin.site.register(CustodyDividend, AdminCostodyDividend)