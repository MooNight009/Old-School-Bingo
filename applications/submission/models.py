from io import BytesIO

from PIL import Image
from django.core.files.storage import default_storage
from django.db import models

from applications.defaults.storage_backends import PublicMediaStorage


class Submission(models.Model):
    # img
    date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=256)
    img = models.ImageField(storage=PublicMediaStorage())  # TODO: SET PROPER PATH FOR STORAGE

    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    team_tile = models.ForeignKey('tile.TeamTile', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.img is not None:
            memfile = BytesIO()
            img = Image.open(self.img)
            img.thumbnail((1000, 1000))
            img.save(memfile, format='PNG', quality=60, optimize=True)
            default_storage.save(self.img.name, memfile)
            memfile.close()
            img.close()


class Reaction(models.Model):
    # reaction = null;
    player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
    submission = models.ForeignKey('submission.Submission', on_delete=models.CASCADE)


class Achievement(models.Model):
    # status = models.CharField(max_length=32, null=False)
    date = models.DateTimeField(auto_now=True)
    team_tile = models.ForeignKey('tile.TeamTile', on_delete=models.CASCADE)
    # player = models.ForeignKey('player.Player', on_delete=models.CASCADE)
