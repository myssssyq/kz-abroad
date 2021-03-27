# Generated by Django 3.1.7 on 2021-03-24 10:32

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0013_auto_20210323_1617'),
        ('accounts', '0025_auto_20210323_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='interest',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
        ),
        migrations.AlterField(
            model_name='occupation',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='occupation_city', to='cities.city'),
        ),
    ]