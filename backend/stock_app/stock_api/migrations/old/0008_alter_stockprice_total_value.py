# Generated by Django 4.0.4 on 2022-05-20 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0007_marketprice_delete_marketindex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockprice',
            name='total_value',
            field=models.BigIntegerField(default=0),
        ),
    ]
