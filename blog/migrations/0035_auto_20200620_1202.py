# Generated by Django 3.0.5 on 2020-06-20 06:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_auto_20200620_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 20, 12, 2, 40, 145715)),
        ),
    ]
