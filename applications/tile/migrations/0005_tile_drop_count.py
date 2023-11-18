# Generated by Django 4.2.7 on 2023-11-18 11:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tile', '0004_tile_pack_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tile',
            name='drop_count',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)]),
        ),
    ]
