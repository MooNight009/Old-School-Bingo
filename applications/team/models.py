from django.db import models

# from applications.player.models import Player
from applications.tile.models import TeamTile


class Team(models.Model):
    team_name = models.CharField(max_length=64)
    score = models.IntegerField(default=0)
    ranking = models.IntegerField(default=-1)

    bingo = models.ForeignKey('bingo.Bingo', on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = False
        if not self.pk:
            is_new = True
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if is_new:
            for tile in self.bingo.get_tiles():
                team_tile = TeamTile(team=self, tile=tile)
                team_tile.save()

    def delete(self, *args, **kwargs):
        for player in self.player_set.all():
            player.teams.remove(self)
            player.teams.add(Team.objects.get(bingo=self.bingo, team_name='General'))
            player.save()
        return super().delete(*args, **kwargs)