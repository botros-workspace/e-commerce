# Generated by Django 3.1.7 on 2021-04-03 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='description'),
            preserve_default=False,
        ),
    ]
