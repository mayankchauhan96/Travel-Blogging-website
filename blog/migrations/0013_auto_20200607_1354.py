# Generated by Django 3.0.5 on 2020-06-07 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200606_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='state_choice',
            new_name='state',
        ),
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]