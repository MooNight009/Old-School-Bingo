import uuid
from PIL import Image
from django.db import models


class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=256)
    img = models.ImageField()  # TODO: SET PROPER PATH FOR STORAGE

    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    team_tile = models.ForeignKey('tile.TeamTile', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        bingo = self.team_tile.tile.bingo
        if bingo.notify_approval:
            bingo.send_discord_message(f'Player **{self.player.user.username}** in team **{self.team_tile.team.team_name}** added submission to **{self.team_tile.tile.name}** with the comment "**{self.comment}"**.')
            self.team_tile.team.send_discord_message(f'**{self.player.user.username}** added submission to **{self.team_tile.tile.name}** with the comment "**{self.comment}"**.')

        if self.img is not None:
            img = Image.open(self.img.path)
            img.thumbnail((1000, 1000))
            img.save(self.img.path, format='PNG', quality=60, optimize=True)

    def __str__(self):
        return f'Submission tile {self.team_tile} by {self.player}'


# class Reaction(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
#     submission = models.ForeignKey('submission.Submission', on_delete=models.CASCADE)


class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now=True)
    team_tile = models.ForeignKey('tile.TeamTile', on_delete=models.CASCADE)
