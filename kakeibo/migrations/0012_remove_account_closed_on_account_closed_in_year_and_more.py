# Generated by Django 4.1 on 2022-08-26 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kakeibo', '0011_alter_account_closed_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='closed_on',
        ),
        migrations.AddField(
            model_name='account',
            name='closed_in_year',
            field=models.IntegerField(default=2022),
        ),
        migrations.AddField(
            model_name='account',
            name='closed_on_month',
            field=models.IntegerField(default=1),
        ),
    ]