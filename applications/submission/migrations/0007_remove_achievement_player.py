# Generated by Django 4.1.7 on 2023-08-19 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0006_achievement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='achievement',
            name='player',
        ),
    ]