from typing import Any, Dict, List
from django.db import models
from django.db.models import Value, F, CheckConstraint, Q
from django.utils.timezone import now
from operator import itemgetter

from ..assets.models import Dividend, Asset
from ..authentication.models import User

class Buy(models.Model):
    volume = models.FloatField(null=False, blank=False)
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE)
    price = models.FloatField(null=False, default=0)
    date = models.DateTimeField(null=False, default=now)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='buys')
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    class Meta():
        constraints = [
            CheckConstraint(check=Q(volume__gte=0), name='buy_volume_non_negative'),
            CheckConstraint(check=Q(price__gte=0), name='buy_price_non_negative')
        ]

    @property
    def total(self) -> float:
        return self.volume * self.price


class Sell(models.Model):
    volume = models.FloatField(null=False, blank=False)
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE)
    price = models.FloatField(null=False, default=0)
    date = models.DateTimeField(null=False, default=now)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='sells')
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    class Meta():
        constraints = [
            CheckConstraint(check=Q(volume__gte=0), name='sell_volume_non_negative'),
            CheckConstraint(check=Q(price__gte=0), name='sell_price_non_negative')
        ]

    @property
    def total(self) -> float:
        return self.volume * self.price
    

class Custody(models.Model):
    volume = models.FloatField(null=False, default=0)
    total_cost = models.FloatField(null=False, default=0)
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    class Meta():
        unique_together = ('asset', 'user')
        constraints = [
            CheckConstraint(check=Q(volume__gte=0), name='custody_volume_non_negative'),
            CheckConstraint(check=Q(total_cost__gte=0), name='custody_total_cost_non_negative')
        ]

    def __str__(self):
        return f"{self.asset.code} - {self.user.username}"

    def rebuild(self):
        params = {'user': self.user, 'asset': self.asset, 'active': True}
        buy_operations = Buy.objects.filter(**params).values('volume', 'price', 'date').annotate(type=Value('buy'))
        sell_operations = Sell.objects.filter(**params).values('volume', 'price', 'date').annotate(type=Value('sell'))
        
        operations: List[Dict[str, Any]] = sorted(list(buy_operations) + list(sell_operations), key=itemgetter('date'))
        total_cost = 0
        volume = 0
        for operation in operations:
            if operation['type'] == 'buy':
                volume += operation['volume']
                total_cost += operation['price'] * operation['volume']
            else:
                if (volume - operation['volume']) < 0:
                    raise ValueError(f"Error on consolidating wallet: The volume became negative in {operation['date']}")
                
                mean_price = total_cost / volume
                total_cost -= mean_price * operation['volume']
                volume -= operation['volume']
        
        self.volume = volume
        self.total_cost = total_cost
        self.save()

    @property
    def last_price(self) -> float:
        return self.asset.last_price()
    
    @property
    def mean_price(self) -> float:
        if self.volume:
            return  self.total_cost / self.volume
        
        return 0
    
    @property
    def dividend_amount_received(self) -> float:
        return sum(self.earned_dividends.all().annotate(
                    sum=F("dividend__value") * F("volume")).values_list('sum', flat=True)
               )

    @property
    def total_value(self) -> float:
        return self.volume * self.last_price
    
    @property
    def balance(self) -> float:
        return self.total_value - self.total_cost
    

class CustodyDividend(models.Model):
    custody = models.ForeignKey(Custody, null=False, on_delete=models.CASCADE, related_name='earned_dividends')
    dividend = models.ForeignKey(Dividend, null=False, on_delete=models.CASCADE)
    volume = models.FloatField(null=False, blank=False, default=0)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    class Meta():
        unique_together = ('custody', 'dividend')
        constraints = [
            CheckConstraint(check=Q(volume__gte=0), name='custody_dividend_volume_non_negative')
        ]

    @property
    def amount_received(self):
        return self.dividend.value * self.volume


class CustodySnapshot(models.Model):
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE)
    date = models.DateField(null=False, default=now)
    volume = models.FloatField(null=False, default=0)
    total_cost = models.FloatField(null=False, default=0)
    last_price = models.FloatField(null=False, default=0)
    mean_price = models.FloatField(null=False, default=0)
    dividend_amount_received = models.FloatField(null=False, default=0)
    total_value = models.FloatField(null=False, default=0)
    balance = models.FloatField(null=False, default=0)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    active = models.BooleanField(null=False, default=True)

    class Meta():
        unique_together = ('asset', 'date')
        constraints = [
            CheckConstraint(check=Q(volume__gte=0), name='custody_snapshot_volume_non_negative'),
            CheckConstraint(check=Q(total_cost__gte=0), name='custody_snapshot_total_cost_non_negative'),
            CheckConstraint(check=Q(last_price__gte=0), name='custody_snapshot_last_price_non_negative'),
            CheckConstraint(check=Q(mean_price__gte=0), name='custody_snapshot_mean_price_non_negative'),
            CheckConstraint(check=Q(dividend_amount_received__gte=0), name='custody_snapshot_dividend_amount_received_non_negative'),
            CheckConstraint(check=Q(total_value__gte=0), name='custody_snapshot_total_value_non_negative'),
            CheckConstraint(check=Q(balance__gte=0), name='custody_snapshot_balance_non_negative')
        ]
