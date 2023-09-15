import datetime

from PIL import Image
from discord import SyncWebhook
from django.db import models
from django.urls import reverse

from applications.submission.models import Achievement
from applications.team.models import Team
from applications.tile.models import Tile

BINGO_TYPES = (
    ('square', 'SQUARE'),
    ('snake', 'SNAKE'),
    ('shootsandladders', 'SHOOTS AND LADDERS'),
)


class Bingo(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)
    img = models.ImageField(null=True, blank=True,
                            help_text="Image displayed in home page")  # TODO: SET PROPER PATH FOR STORAGE

    start_date = models.DateTimeField(help_text="Starting date and time of bingo. UTC not local timezone")
    end_date = models.DateTimeField(help_text="Starting date and time of bingo. UTC not local timezone")
    is_game_over_on_finish = models.BooleanField(default=False,
                                                 help_text="Does the game finish when a team reaches maximum points? (Not implemented)")

    is_ready = models.BooleanField(default=False)  # Is the game ready to start
    is_started = models.BooleanField(default=False)  # Has is the game started
    is_over = models.BooleanField(default=False)  # Is the game over

    is_public = models.BooleanField(default=False,
                                    help_text="Can someone who hasn't joined the bingo see it? (Not implemented)")  # Is the game public
    is_team_public = models.BooleanField(default=False,
                                         help_text="Can a player view other teams' boards? (Not fully tested)")  # Status of team public
    is_row_col_extra = models.BooleanField(default=True,
                                           help_text="Do teams get extra points for completing a row or column?")  # Whether players get extra point for finishing a full row/column

    can_players_create_team = models.BooleanField(default=True,
                                                  help_text="Can the players create the own teams?")
    max_players_in_team = models.IntegerField(default=0,
                                              help_text="If players can create their teams what is the maximum team size? (0 Means no limit)")

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

    winner = models.OneToOneField('team.Team', on_delete= models.SET_NULL, null=True, related_name='bingo_winner_team')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.img is not None:
            img = Image.open(self.img.path)
            img.thumbnail((270, 200))
            img.save(self.img.path, format='PNG', quality=60, optimize=True)

    # TODO: Actually implement method
    def get_is_started(self):
        if not self.is_started:
            if self.start_date <= datetime.datetime.now(datetime.timezone.utc):
                self.is_started = True
                self.winner = None
                self.save()
        return self.is_started

    def get_is_over(self):
        if not self.is_over:
            change = self.end_date <= datetime.datetime.now(datetime.timezone.utc)
            if change != self.is_over:
                self.is_over = change
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
                last_achievement = Achievement.objects.filter(team_tile__team=team).order_by('-date').first()
                dict[team] = last_achievement

            for team in top_teams:
                if dict[team].date < dict[first_team].date:
                    first_team = team

            self.winner = first_team

        self.winner = top_teams.first()
        self.save()
        return self.winner

    def send_discord_message(self, message):
        try:
            webhook = SyncWebhook.from_url(self.discord_webhook)
            webhook.send(message)
        except ValueError:
            print("Sending discord message failed") # TODO: Better error logging method