# Generated by Django 4.2.7 on 2023-11-03 20:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bingo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Text limit: 64 Characters', max_length=64)),
                ('description', models.TextField(help_text='Text limit: 2048 Characters', max_length=2048)),
                ('img', models.ImageField(blank=True, help_text='Image displayed in home page. Recommended size: 270x200px', null=True, upload_to='')),
                ('start_date', models.DateTimeField(help_text='Starting date and time of bingo.')),
                ('end_date', models.DateTimeField(help_text='Starting date and time of bingo.')),
                ('is_game_over_on_finish', models.BooleanField(default=False, help_text='Does the game finish when a team reaches maximum points? (Not implemented)')),
                ('is_ready', models.BooleanField(default=False)),
                ('is_started', models.BooleanField(default=False)),
                ('is_over', models.BooleanField(default=False)),
                ('is_public', models.BooleanField(default=False, help_text="Can someone who hasn't joined the bingo see it? (Not implemented)")),
                ('is_team_public', models.BooleanField(default=False, help_text="Can a player view other teams' boards? (Not fully tested)")),
                ('is_row_col_extra', models.BooleanField(default=True, help_text='Do teams get extra points for completing a row or column?')),
                ('can_players_create_team', models.BooleanField(default=True, help_text='Can the players create the own teams?')),
                ('max_players_in_team', models.IntegerField(default=0, help_text='If players can create their teams what is the maximum team size? (0 Means no limit)')),
                ('board_type', models.CharField(choices=[('square', 'SQUARE'), ('snake', 'SNAKE'), ('shootsandladders', 'SHOOTS AND LADDERS')], default='square', help_text='Board type (Not implemented)', max_length=16)),
                ('board_size', models.IntegerField(default=5, help_text='Width/Height size of the board. THIS CANNOT BE CHANGED LATER')),
                ('max_score', models.IntegerField(default=-1)),
                ('enable_discord', models.BooleanField(default=False, help_text='Should you be notified via discord when something changes?')),
                ('discord_webhook', models.CharField(blank=True, help_text='Webhook URL for your channel.', max_length=256)),
                ('notify_submission', models.BooleanField(default=False, help_text='Should you be notified when someone submits a new picture?')),
                ('notify_completion', models.BooleanField(default=False, help_text='Should you be notified when someone completes a tile?')),
                ('notify_approval', models.BooleanField(default=False, help_text='Should you be notified when someone approves a tile?')),
            ],
        ),
    ]
