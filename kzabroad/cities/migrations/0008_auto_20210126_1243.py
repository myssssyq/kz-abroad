# Generated by Django 3.0.8 on 2021-01-26 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0007_auto_20210113_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='picture',
            field=models.CharField(max_length=200),
        ),
    ]