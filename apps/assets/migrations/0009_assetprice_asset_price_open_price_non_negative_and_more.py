# Generated by Django 5.1.5 on 2025-02-08 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_assets', '0008_assetprice_volume'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='assetprice',
            constraint=models.CheckConstraint(condition=models.Q(('volume__gte', 0)), name='asset_price_volume_non_negative'),
        ),
        migrations.AddConstraint(
            model_name='dividend',
            constraint=models.CheckConstraint(condition=models.Q(('value__gte', 0)), name='dividend_value_non_negative'),
        ),
    ]
