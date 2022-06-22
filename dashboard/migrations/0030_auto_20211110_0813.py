# Generated by Django 3.2.8 on 2021-11-10 08:13

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_auto_20211110_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 10, 8, 13, 49, 493089), null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]