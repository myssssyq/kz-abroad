# Generated by Django 3.0.8 on 2021-03-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_occupation_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_admin',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
