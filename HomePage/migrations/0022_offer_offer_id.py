# Generated by Django 3.0.1 on 2020-07-17 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0021_offer_offer_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='offer_id',
            field=models.CharField(default='', max_length=50),
        ),
    ]
