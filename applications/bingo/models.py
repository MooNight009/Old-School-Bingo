import datetime
import uuid

import requests
from PIL import Image
from discord import SyncWebhook
from django.db import models
from django.urls import reverse

from applications.submission.models import Achievement
from applications.team.models import Team
from applications.tile.models import Tile, TeamTile
from common.wiseoldman.wiseoldman import update_competition

BINGO_TYPES = (
    ('square', 'SQUARE'),
    ('snake', 'SNAKE'),
    ('shootsandladders', 'SHOOTS AND LADDERS'),
)


class Bingo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, help_text='Text limit: 64 Characters')
    description = models.TextField(max_length=2048, help_text='Text limit: 2048 Characters')
    img = models.ImageField(null=True, blank=True,
                            help_text="Image displayed in home page. Recommended size: 270x200px")  # TODO: SET PROPER PATH FOR STORAGE

    start_date = models.DateTimeField(help_text="Starting date and time of bingo.")
    end_date = models.DateTimeField(help_text="Starting date and time of bingo.")
    is_game_over_on_finish = models.BooleanField(default=False,
                                                 help_text="Does the game finish when a team reaches maximum points? (Not implemented)")

    is_ready = models.BooleanField(default=False)  # Is the game ready to start
    is_started = models.BooleanField(default=False)  # Has is the game started
    is_over = models.BooleanField(default=False)  # Is the game over

    is_public = models.BooleanField(default=False,
                                    help_text="Make the bingo visible from main page")  # Is the game public
    is_team_public = models.BooleanField(default=False,
                                         help_text="Can players view other teams' boards?")  # Status of team public
    is_row_col_extra = models.BooleanField(default=True,
                                           help_text="Do teams get extra points for completing a row or column?")  # Whether players get extra point for finishing a full row/column

    can_players_create_team = models.BooleanField(default=True,
                                                  help_text="Can the players create the own teams?")
    max_players_in_team = models.IntegerField(default=10,
                                              help_text="What is the maximum number of players in a team")

    board_type = models.CharField(max_length=16, choices=BINGO_TYPES, default='square',
                                  help_text="Board type (Not implemented)")
    board_size = models.IntegerField(default=5,
                                     help_text="Width/Height size of the board. THIS CANNOT BE CHANGED LATER")

    max_score = models.IntegerField(default=-1)

    enable_discord = models.BooleanField(default=False,
                                         help_text="Should you be notified via discord when something changes?")
    discord_webhook = models.CharField(blank=True, max_length=256,
                                       help_text="Webhook URL for your channel.")
    notify_submission = models.BooleanField(default=False,
                                            help_text="Should you be notified when someone submits a new picture?")
    notify_completion = models.BooleanField(default=False,
                                            help_text="Should you be notified when someone completes a tile?")
    notify_approval = models.BooleanField(default=False,
                                          help_text="Should you be notified when someone approves a tile?")

    winner = models.OneToOneField('team.Team', on_delete=models.SET_NULL, null=True, related_name='bingo_winner_team')

    competition_id = models.CharField(max_length=64, default="")
    competition_verification_code = models.CharField(max_length=64, default="")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.img is not None:
            img = Image.open(self.img.path)
            img = img.resize((270, 200))
            img.save(self.img.path, format='PNG', quality=60, optimize=True)

    def __str__(self):
        return self.name

    # TODO: Actually implement method
    def get_is_started(self):
        if not self.is_started:
            if self.start_date <= datetime.datetime.now(datetime.timezone.utc):
                self.is_started = True
                self.winner = None
                self.save()

                # Update every player detail
                players_details = self.playerbingodetail_set.all()
                for players_detail in players_details:
                    names = players_detail.account_names.split(',')
                    for name in names:
                        response = requests.post(f'https://api.wiseoldman.net/v2/players/{name}/')
                        if response.status_code != 200:
                            print("We got an error in player " + name)
                update_competition(self)
        return self.is_started

    def get_is_over(self):
        if not self.is_over:
            change = self.end_date <= datetime.datetime.now(datetime.timezone.utc)
            if change != self.is_over:
                self.is_over = change
                self.is_team_public = True
                self.is_public = True
                self.save()
        return self.is_over

    def get_tiles(self):
        return Tile.objects.filter(bingo=self).order_by('bingo_location').all()

    def get_column_width(self):
        return 100 / self.board_size

    def get_div_width(self):
        return self.board_size * 150

    def get_join_link(self):
        return reverse('bingo:join_bingo', kwargs={'pk': self.id})

    def get_img_url(self):
        if self.img:
            return self.img.url
        else:
            return 'https://www.thesportsdb.com/images/media/league/trophy/x6hlig1575731898.png'

    def get_winner(self):
        if self.winner is not None:
            return self.winner
        top_teams = self.team_set.filter(ranking=1).exclude(team_name='General')
        if top_teams.count() > 1:
            dict = {}
            first_team = top_teams.first()
            for team in top_teams:
                last_achievement = TeamTile.objects.filter(team=team).order_by('-completion_date').first()
                dict[team] = last_achievement

            for team in top_teams:
                if dict[team].date < dict[first_team].date:
                    first_team = team

            self.winner = first_team
        elif top_teams.count() == 0:
            top_teams = self.team_set.filter(team_name='General')

        self.winner = top_teams.first()
        self.save()
        return self.winner

    def send_discord_message(self, message):
        try:
            webhook = SyncWebhook.from_url(self.discord_webhook)
            webhook.send(message)
        except ValueError:
            print("Sending discord message failed")  # TODO: Better error logging method

    def calculate_max_score(self):
        max_score = 0
        for tile in self.tile_set.all():
            max_score += tile.score

        if self.is_row_col_extra:
            max_score += (self.board_size * 2)

        self.max_score = max_score
        self.save()
        return max_score
