# Generated by Django 3.0.8 on 2020-12-23 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20201219_1526'),
        ('cities', '0005_city_guide_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidesession',
            name='guide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='guide', to='accounts.Account'),
        ),
    ]
