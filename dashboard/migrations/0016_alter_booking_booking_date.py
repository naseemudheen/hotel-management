# Generated by Django 3.2.8 on 2021-10-29 12:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_auto_20211029_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 10, 29, 12, 35, 19, 990976), null=True),
        ),
    ]