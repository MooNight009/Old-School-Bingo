# Generated by Django 4.2.7 on 2023-11-03 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bingo', '0001_initial'),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bingo',
            name='winner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bingo_winner_team', to='team.team'),
        ),
    ]
