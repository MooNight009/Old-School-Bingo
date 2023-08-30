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
