# Generated by Django 3.1.7 on 2021-03-23 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_auto_20210323_1442'),
        ('cities', '0011_auto_20210323_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='guides',
            field=models.ManyToManyField(blank=True, related_name='guides', to='accounts.Account'),
        ),
    ]
