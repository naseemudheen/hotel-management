# Generated by Django 3.2.8 on 2021-11-09 10:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0025_alter_booking_booking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 9, 10, 3, 2, 540175), null=True),
        ),
    ]