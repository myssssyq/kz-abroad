# Generated by Django 3.1.7 on 2021-03-24 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_auto_20210324_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='interest',
            field=models.JSONField(blank=True, default=None),
        ),
    ]
