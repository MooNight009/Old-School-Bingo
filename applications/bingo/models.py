import datetime

from io import BytesIO
from PIL import Image
from django.core.files.storage import default_storage
from django.db import models
from django.urls import reverse

from applications.defaults.storage_backends import PublicMediaStorage
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
    img = models.ImageField(null=True, blank=True, storage=PublicMediaStorage()) # TODO: SET PROPER PATH FOR STORAGE
    description = models.TextField(max_length=2048)
    img = models.ImageField(null=True, blank=True, storage=PublicMediaStorage())  # TODO: SET PROPER PATH FOR STORAGE

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_game_over_on_finish = models.BooleanField(default=False)

    is_ready = models.BooleanField(default=False)  # Is the game ready to start
    is_started = models.BooleanField(default=False)  # Has is the game started
    is_over = models.BooleanField(default=False)  # Is the game over
    is_public = models.BooleanField(default=False)  # Is the game public
    is_team_public = models.BooleanField(default=False)  # Status of team public

    can_players_create_team = models.BooleanField(default=True)
    max_players_in_team = models.IntegerField(default=0)

    board_type = models.CharField(max_length=16, choices=BINGO_TYPES, default='square')
    board_size = models.IntegerField(default=10)

    max_score = models.IntegerField(default=-1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.img is not None:
            memfile = BytesIO()
            img = Image.open(self.img)
            img.thumbnail((270, 200))
            img.save(memfile, format='PNG', quality=60, optimize=True)
            default_storage.save(self.img.name, memfile)
            memfile.close()
            img.close()

    # TODO: Actually implement method
    def get_is_started(self):
        if not self.is_started:
            change = self.start_date <= datetime.datetime.now(datetime.timezone.utc)
            if change != self.is_started:
                self.is_started = change
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
        top_teams = self.team_set.filter(ranking=1)
        if top_teams.count() > 1:
            dict = {}
            first_team = top_teams.first()
            for team in top_teams:
                last_achievement = Achievement.objects.filter(team_tile__team=team).order_by('-date').first()
                dict[team] = last_achievement

            for team in top_teams:
                if dict[team].date < dict[first_team].date:
                    first_team = team

            return first_team

        return top_teams.first()
