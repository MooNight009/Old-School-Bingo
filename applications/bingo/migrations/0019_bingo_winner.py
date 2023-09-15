# Generated by Django 4.1.7 on 2023-09-15 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_alter_team_ranking'),
        ('bingo', '0018_bingo_discord_webhook_bingo_enable_discord_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bingo',
            name='winner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bingo_winner_team', to='team.team'),
        ),
    ]