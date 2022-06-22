# Generated by Django 3.2.8 on 2021-10-30 11:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_auto_20211030_0908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedroom',
            name='adult',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 30, 11, 9, 16, 972368), null=True),
        ),
    ]