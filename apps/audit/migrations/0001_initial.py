# Generated by Django 5.1.4 on 2024-12-29 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(max_length=100)),
                ('object_id', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('old_values', models.TextField()),
            ],
        ),
    ]
