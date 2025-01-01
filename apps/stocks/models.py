from django.db import models
from datetime import datetime, timedelta

class StockType(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.name
    

class StockSubType(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    stock_type = models.ForeignKey(StockType, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.name

#TODO change name to asset (refactor needed in many places)
class Stock(models.Model):
    code = models.CharField(max_length=10, blank=False, null=False, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    stock_sub_type = models.ForeignKey(StockSubType, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.code
    
    def current_price(self):
        stock_price = StockPrice.objects.filter(stock=self).order_by('-date').first()
        if stock_price:
            return stock_price.mean_price

        return 0
    
    @property
    def has_dividends(self) -> bool:
        threshold_date = datetime.today().date() - timedelta(days=120)
        return self.dividends.filter(date__gte=threshold_date).exists()


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    min_price = models.FloatField(null=False, default=0)
    max_price = models.FloatField(null=False, default=0)
    date = models.DateField(null=False, auto_now=True)

    class Meta():
        unique_together = ("stock", "date")

    @property
    def mean_price(self) -> float:
        return (self.max_price + self.min_price) / 2


class Dividend(models.Model):
    stock = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE, related_name='dividends')
    value = models.FloatField(null=False)
    date = models.DateField(null=False, auto_now=True)

    class Meta():
        unique_together = ("stock", "date")

    def __str__(self):
        return f"{self.stock} - {self.date}"