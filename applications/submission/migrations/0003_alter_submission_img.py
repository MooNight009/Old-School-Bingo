# Generated by Django 4.2.7 on 2023-11-04 15:34

import applications.defaults.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='img',
            field=models.ImageField(storage=applications.defaults.storage_backends.PublicMediaStorage(), upload_to=''),
        ),
    ]