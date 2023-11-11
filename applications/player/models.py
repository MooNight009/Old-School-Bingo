import uuid

from django.contrib.auth.models import User
from django.db import models

from applications.bingo.models import Bingo
from applications.team.models import Team


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Moderator(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=True, related_name='moderator_player')
    bingo = models.ForeignKey(Bingo, on_delete=models.CASCADE, null=False, related_name='moderator_bingo')

    def __str__(self):
        return f'Moderator {self.player} in {self.bingo}'


class PlayerBingoDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    """
        Stores details for every player's bingo
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, null=False)
    bingo = models.ForeignKey(Bingo, on_delete=models.CASCADE, null=False)
    account_names = models.CharField(max_length=512, blank=True, default='')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # if self.account_names == '':
        #     self.account_names = self.player.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f'PlayerDetail {self.player} in {self.bingo}'
