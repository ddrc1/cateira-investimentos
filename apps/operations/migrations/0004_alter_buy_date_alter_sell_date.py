# Generated by Django 5.1.4 on 2024-12-30 16:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_operations', '0003_remove_custody_mean_price_custody_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sell',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
