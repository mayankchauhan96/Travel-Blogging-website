# Generated by Django 3.0.5 on 2021-01-07 18:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210108_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 8, 0, 10, 34, 825569)),
        ),
    ]
