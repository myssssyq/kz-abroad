# Generated by Django 3.0.8 on 2021-01-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0006_auto_20201223_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidesession',
            name='status',
            field=models.CharField(blank=True, choices=[('Waiting', 'Waiting'), ('Needs approve', 'Needs approve'), ('In process', 'In process'), ('Finished', 'Finished')], max_length=15),
        ),
    ]
