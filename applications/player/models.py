from django.contrib.auth.models import User
from django.db import models

from applications.bingo.models import Bingo
from applications.team.models import Team


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bingos = models.ManyToManyField(Bingo)
    teams = models.ManyToManyField(Team)


class Moderator(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='moderator_player')
    bingo = models.ForeignKey(Bingo, on_delete=models.CASCADE, null=False, related_name='moderator_bingo')


class PlayerBingoDetail(models.Model):
    """
        Stores details for every player's bingo
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    bingo = models.ForeignKey(Bingo, on_delete=models.CASCADE, null=False)
    account_names = models.CharField(max_length=512, blank=True, default='')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.account_names == '':
            self.account_names = self.player.user.username
        super().save(*args, **kwargs)
