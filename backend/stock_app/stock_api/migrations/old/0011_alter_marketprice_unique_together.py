# Generated by Django 4.0.4 on 2022-05-23 05:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0010_alter_stockprice_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='marketprice',
            unique_together={('market_symbol', 'trading_date')},
        ),
    ]
