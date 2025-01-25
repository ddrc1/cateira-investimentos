from typing import Optional
from django.db import models
from datetime import datetime, timedelta
from yfinance import Ticker

class Sector(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.name
    

class SubSector(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    sector = models.ForeignKey(Sector, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.name
    
class AssetType(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    code = models.CharField(max_length=100, blank=False, null=False)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sub_sector = models.ForeignKey(SubSector, null=True, on_delete=models.CASCADE)
    asset_type = models.ForeignKey(AssetType, null=False, on_delete=models.CASCADE)
    country = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    class Meta():
        unique_together = ("code", "asset_type")

    def __str__(self):
        return self.code
    
    # def save(self):
    #     if not self.description or not self.country or not self.businessSummary:
    #         ticker: Ticker = self.get_ticker_object()
    #         ticker_info: dict = ticker.info

    #         if not self.description:
    #             self.description = ticker_info['longName']
            
    #         if not self.country:
    #             self.country = ticker_info['country']
            
    #         if not self.businessSummary:
    #             self.businessSummary = ticker_info['longBusinessSummary']

    #     return super().save()
    
    def last_price(self):
        last_price: Optional[AssetPrice] = self.prices.order_by('date').last()
        if last_price:
            return last_price.close_price

        return 0
    
    @property
    def has_dividends(self) -> bool:
        threshold_date = datetime.today().date() - timedelta(days=120)
        return self.dividends.filter(date__gte=threshold_date).exists()


class AssetPrice(models.Model):
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE, related_name='prices')
    open_price = models.FloatField(null=False, default=0)
    high_price = models.FloatField(null=False, default=0)
    low_price = models.FloatField(null=False, default=0)
    close_price = models.FloatField(null=False, default=0)
    volume = models.FloatField(null=False, default=0)
    date = models.DateField(null=False)

    class Meta():
        unique_together = ("asset", "date")

    @property
    def mean_price(self) -> float:
        return (self.high_price + self.low_price) / 2


class Dividend(models.Model):
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE, related_name='dividends')
    value = models.FloatField(null=False)
    date = models.DateField(null=False)

    class Meta():
        unique_together = ("asset", "date")

    def __str__(self):
        return f"{self.asset} - {self.date}"