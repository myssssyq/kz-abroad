# Generated by Django 3.0.8 on 2020-11-26 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20201107_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='slug',
            field=models.SlugField(default=None, max_length=200),
        ),
    ]
