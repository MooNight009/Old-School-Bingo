# Generated by Django 4.1.7 on 2023-09-16 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invocation', '0004_wosinvo_amount_wosinvo_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissioninvo',
            name='tile',
        ),
        migrations.RemoveField(
            model_name='wosinvo',
            name='tile',
        ),
    ]