# Generated by Django 3.0.8 on 2020-12-02 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_account_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='recieved_requests',
            field=models.ManyToManyField(related_name='_account_recieved_requests_+', to='accounts.Account'),
        ),
        migrations.AddField(
            model_name='account',
            name='sent_requests',
            field=models.ManyToManyField(related_name='_account_sent_requests_+', to='accounts.Account'),
        ),
        migrations.DeleteModel(
            name='FriendRequest',
        ),
    ]
