# Generated by Django 4.1.7 on 2023-09-16 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invocation', '0007_submissioninvo_tile_wominvo_tile'),
    ]

    operations = [
        migrations.AddField(
            model_name='wominvo',
            name='names',
            field=models.CharField(default='', max_length=256),
        ),
    ]
