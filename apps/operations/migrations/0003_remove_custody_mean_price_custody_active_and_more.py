# Generated by Django 5.1.4 on 2024-12-30 14:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps_operations', '0002_alter_buy_user_alter_sell_user_custody'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custody',
            name='mean_price',
        ),
        migrations.AddField(
            model_name='custody',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='custody',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='custody',
            name='total_cost',
            field=models.FloatField(default=0, help_text='Amount spent for this stock'),
        ),
        migrations.AddField(
            model_name='custody',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='custody',
            name='volume',
            field=models.PositiveIntegerField(default=0, help_text='Amount in custody'),
        ),
    ]
