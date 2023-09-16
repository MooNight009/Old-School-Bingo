import datetime
from abc import abstractmethod

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Invocation(models.Model):
    tile = models.OneToOneField('tile.Tile', on_delete=models.CASCADE, null=True)
    class Meta:
        abstract= True


    @abstractmethod
    def update_complete(self, team_tile):
        pass

    @abstractmethod
    def update_approve(self, team_tile):
        pass


class SubmissionInvo(Invocation):

    def update_complete(self, team_tile, username):
        team_tile.is_complete = not team_tile.is_complete
        bingo = self.tile.bingo

        if bingo.notify_completion:
            bingo.send_discord_message(
                f'Player **{username}** set the status of **{team_tile.tile.name}** completion to **{team_tile.is_complete}**.')

        if team_tile.is_complete:
            team_tile.completion_date = datetime.datetime.now(datetime.timezone.utc)

        team_tile.save()

    def update_approve(self, team_tile, username):
        bingo = self.tile.bingo
        team_tile.is_mod_approved = not team_tile.is_mod_approved

        if bingo.notify_approval:
            bingo.send_discord_message(
                f'Moderator **{username}** set the status of **{team_tile.tile.name}** approval to **{team_tile.is_complete}**.')
        pass

class WOMInvo(Invocation):
    TYPES = [
        ('XP', 'Skilling'),
        ('KC', 'Bossing'),
        ('LV', 'Levels')
    ]

    type = models.CharField(max_length=2, default='LV', choices=TYPES)
    amount = models.IntegerField(default=1)
    names = models.CharField(max_length=256, default='')
