# Generated by Django 4.1.7 on 2023-10-13 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0022_alter_bingo_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bingo',
            name='description',
            field=models.TextField(help_text='Text limit: 2048 Characters', max_length=2048),
        ),
        migrations.AlterField(
            model_name='bingo',
            name='name',
            field=models.CharField(help_text='Text limit: 64 Characters', max_length=64),
        ),
    ]