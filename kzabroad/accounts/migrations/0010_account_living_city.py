# Generated by Django 3.0.8 on 2020-12-15 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0002_city_slug'),
        ('accounts', '0009_auto_20201202_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='living_city',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='city', to='cities.City'),
        ),
    ]
