# Generated by Django 4.1.7 on 2023-09-03 19:17

import applications.defaults.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tile', '0011_alter_tile_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tile',
            name='img',
            field=models.ImageField(blank=True, null=True, storage=applications.defaults.storage_backends.PublicMediaStorage(), upload_to=''),
        ),
    ]
