# Generated by Django 4.1.7 on 2023-09-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0012_alter_bingo_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bingo',
            name='description',
            field=models.TextField(max_length=2048),
        ),
    ]