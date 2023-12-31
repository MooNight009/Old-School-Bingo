# Generated by Django 4.2.7 on 2023-11-18 12:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tile', '0005_tile_drop_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='drop_count',
            field=models.IntegerField(default=1, help_text='Number of drops, ignore if using WOM tracker', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)]),
        ),
    ]
