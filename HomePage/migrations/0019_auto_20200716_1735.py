# Generated by Django 3.0.1 on 2020-07-16 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0018_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='bestseller',
            name='bestseller_desc',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='bestseller',
            name='bestseller_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='brand_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_price',
            field=models.FloatField(default=0),
        ),
    ]
