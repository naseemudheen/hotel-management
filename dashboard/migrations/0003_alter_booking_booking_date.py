# Generated by Django 3.2.8 on 2021-10-23 11:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_booking_booking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 10, 23, 11, 21, 27, 924913), null=True),
        ),
    ]
