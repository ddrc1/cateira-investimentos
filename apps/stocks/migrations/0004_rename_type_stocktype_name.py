# Generated by Django 5.1.4 on 2025-01-01 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps_stocks', '0003_alter_dividend_stock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocktype',
            old_name='type',
            new_name='name',
        ),
    ]