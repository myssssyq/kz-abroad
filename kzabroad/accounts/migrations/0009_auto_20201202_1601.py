# Generated by Django 3.0.8 on 2020-12-02 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20201202_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='recieved_requests',
        ),
        migrations.RemoveField(
            model_name='account',
            name='sent_requests',
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='accounts.Account')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='accounts.Account')),
            ],
        ),
    ]
