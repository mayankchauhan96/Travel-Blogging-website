# Generated by Django 3.0.5 on 2020-06-19 04:13

import datetime
from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_auto_20200615_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='postview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 19, 9, 43, 50, 411650)),
        ),
    ]