# Generated by Django 3.2.8 on 2021-11-10 08:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_alter_booking_booking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 10, 8, 24, 12, 991917), null=True),
        ),
    ]
