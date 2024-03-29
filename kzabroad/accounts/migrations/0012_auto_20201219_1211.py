# Generated by Django 3.0.8 on 2020-12-19 12:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20201215_1233'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prefereneces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='account',
            name='prefereneces',
            field=models.ManyToManyField(blank=True, to='accounts.Prefereneces'),
        ),
    ]
