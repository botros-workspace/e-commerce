# Generated by Django 3.1.7 on 2021-04-03 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210403_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='Product'),
            preserve_default=False,
        ),
    ]
