# Generated by Django 4.1.7 on 2023-08-27 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0007_alter_bingo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='bingo',
            name='img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]