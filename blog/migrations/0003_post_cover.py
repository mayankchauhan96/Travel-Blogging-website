# Generated by Django 3.0.5 on 2020-04-17 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
