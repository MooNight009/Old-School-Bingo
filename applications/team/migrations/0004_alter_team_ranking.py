# Generated by Django 4.1.7 on 2023-09-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_rename_bingo_score_team_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='ranking',
            field=models.IntegerField(default=1),
        ),
    ]