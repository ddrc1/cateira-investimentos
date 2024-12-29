from django.db import models
from django.utils.timezone import now
from django.db.models import QuerySet

from ..stocks.models import Stock
from ..authentication.models import User

class Wallet(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='wallet')
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.user.username

    def buy_operations(self) -> QuerySet['Buy']:
        return self.buys.filter(active=True)
    
    def sell_operations(self) -> QuerySet['Sell']:
        return self.sells.filter(active=True)
    

class Buy(models.Model):
    volume = models.PositiveIntegerField(null=False, blank=False)
    stock = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    price = models.FloatField(null=False, default=0)
    date = models.DateField(null=False, default=now)
    wallet = models.ForeignKey(Wallet, null=False, on_delete=models.CASCADE, related_name='buys')
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)


class Sell(models.Model):
    volume = models.PositiveIntegerField(null=False, blank=False)
    stock = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    price = models.FloatField(null=False, default=0)
    date = models.DateField(null=False, default=now)
    wallet = models.ForeignKey(Wallet, null=False, on_delete=models.CASCADE, related_name='sells')
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)
