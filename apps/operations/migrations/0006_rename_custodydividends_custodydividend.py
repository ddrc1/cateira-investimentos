# Generated by Django 5.1.4 on 2024-12-30 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps_operations', '0005_custodydividends'),
        ('apps_stocks', '0003_alter_dividend_stock'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustodyDividends',
            new_name='CustodyDividend',
        ),
    ]