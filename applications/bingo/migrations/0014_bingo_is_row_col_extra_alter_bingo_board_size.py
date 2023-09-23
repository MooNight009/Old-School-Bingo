# Generated by Django 4.1.7 on 2023-09-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bingo', '0013_alter_bingo_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='bingo',
            name='is_row_col_extra',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='bingo',
            name='board_size',
            field=models.IntegerField(default=5),
        ),
    ]
