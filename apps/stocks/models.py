from django.db import models

class StockType(models.Model):
    type = models.CharField(max_length=50, blank=False, null=False, unique=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.type


class Stock(models.Model):
    code = models.CharField(max_length=10, blank=False, null=False, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    stock_type = models.ForeignKey(StockType, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, null=False)
    updated_at = models.DateTimeField(auto_now_add=True, null=False)
    active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.code


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    min_price = models.FloatField(null=False, default=0)
    max_price = models.FloatField(null=False, default=0)
    date = models.DateField(null=False, auto_now=True)

    class Meta():
        unique_together = ("stock", "date")


class Dividends(models.Model):
    stock = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    value = models.FloatField(null=False)
    date = models.DateField(null=False, auto_now=True)

    class Meta():
        unique_together = ("stock", "date")