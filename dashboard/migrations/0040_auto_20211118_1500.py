# Generated by Django 3.2.8 on 2021-11-18 09:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0039_alter_booking_booking_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='notifications',
            new_name='Notification',
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 18, 15, 0, 42, 35821), null=True),
        ),
    ]
