# Generated by Django 3.2.8 on 2021-10-26 07:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20211026_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 10, 26, 7, 28, 22, 497334), null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]