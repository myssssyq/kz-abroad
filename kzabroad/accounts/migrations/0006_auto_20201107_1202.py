# Generated by Django 3.0.8 on 2020-11-07 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201107_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='cost_preference',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]
