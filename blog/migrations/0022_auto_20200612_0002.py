# Generated by Django 3.0.5 on 2020-06-11 18:32

import ckeditor.fields
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20200608_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(blank=True, choices=[('Beaches', 'Beaches'), ('Islands', 'Islands'), ('Hiking', 'Hiking'), ('Camping', 'Camping'), ('Mountains', 'Mountains'), ('Deserts', 'Deserts'), ('Forests', 'Forests'), ('Historic Places', 'Historic Places'), ('Monuments', 'Monuments'), ('Temples', 'Temples'), ('Museums', 'Museums'), ('Zoos', 'Zoos'), ('Theme Parks', 'Theme Parks'), ('Gardens', 'Gardens'), ('Aquaria', 'Aquaria'), ('Winter', 'Winter Carnival'), ('Markets & Shopping', 'Markets & Shopping'), ('Urban', 'Urban'), ('Rural', 'Rural'), ('Rivers & Lakes', 'Rivers & Lakes'), ('Couples Friendly', 'Couples Friendly'), ('Sports Tourism', 'Sports Tourism'), ('Just for Food', 'Just for Food '), ('Resorts', 'Resorts'), ('Culture', 'Culture'), ('Adventure', 'Adventure'), ('Moto Blogs', 'Moto Blogs'), ('Solo', 'Solo Travel'), ('Summer', 'Summer Special'), ('Travel Tips', 'Travel Tips')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=400, unique=True),
        ),
        migrations.AlterField(
            model_name='postview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 12, 0, 2, 20, 902154)),
        ),
    ]