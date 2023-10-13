from PIL import Image
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from applications.invocation.models import SubmissionInvo


class Tile(models.Model):
    bingo = models.ForeignKey('bingo.Bingo', on_delete=models.CASCADE)

    name = models.CharField(max_length=64, default="Tile Name",
                            help_text='Text limit: 64 Characters, Recommended less than 16')
    description = models.TextField(max_length=512, default="Description", help_text='Text limit: 512 Characters')
    img = models.ImageField(null=True, blank=True,
                            help_text="Image associated with Tile. Recommended size: 270x200px")  # TODO: SET PROPER PATH FOR STORAGE

    bingo_location = models.IntegerField()
    score = models.IntegerField(default=1)
    is_ready = models.BooleanField(default=False)

    # Invocation details
    INVOCATION_TYPES = [
        ('SBM', "Submission"),
        ('WOM', "WiseOldMan")
    ]
    invocation_type = models.CharField(max_length=3, default='SBM', choices=INVOCATION_TYPES)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    invocation = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            invocation = SubmissionInvo.objects.create()
            self.invocation = invocation
        super().save(*args, **kwargs)
        if self.img is not None and self.img.name is not None and len(self.img.name) != 0:
            img = Image.open(self.img.path)
            img.thumbnail((270, 200))
            img.save(self.img.path, format='PNG', quality=60, optimize=True)

        # Make board ready if all tiles are ready
        # TODO: Add better way of checking whether everything is set
        if not Tile.objects.filter(bingo=self.bingo, is_ready=False).exists():
            self.bingo.is_ready = True
            self.bingo.save()

        if is_new:
            self.invocation.tile = self
            self.invocation.save()

    def get_ready_color(self):
        if self.is_ready:
            return 'bg-success-subtle'
        return 'bg-danger-subtle'

    def get_completed_count(self):
        total = TeamTile.objects.filter(tile=self).exclude(team__team_name='General')
        completed = total.filter(is_complete=True)
        return f"{completed.count()}/{total.count()}"

    def get_approved_count(self):
        total = TeamTile.objects.filter(tile=self).exclude(team__team_name='General')
        approved = total.filter(is_mod_approved=True)
        return f"{approved.count()}/{total.count()}"

    def get_tile_general_color(self):
        total = TeamTile.objects.filter(tile=self).exclude(team__team_name='General')
        approved_count = total.filter(is_mod_approved=True).count()
        completed_count = total.filter(is_complete=True).count()
        color = ''
        # If we have unapproved tiles
        if approved_count < completed_count:
            color = 'border-red3'
        elif approved_count == total.count():
            color = 'border-green3'
        elif approved_count >= (total.count() / 2):
            color = 'border-success-subtle'

        return color

    def get_url(self):
        if self.img:
            return self.img.url
        else:
            return ''


class TeamTile(models.Model):
    is_current = models.BooleanField(default=True)
    is_skipped = models.BooleanField(default=False)

    is_complete = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True)

    is_mod_approved = models.BooleanField(default=False)
    mod_approval_date = models.DateTimeField(null=True)

    team = models.ForeignKey('team.Team', on_delete=models.CASCADE)
    tile = models.ForeignKey('tile.Tile', on_delete=models.CASCADE)

    score = models.IntegerField(default=0)

    def is_complete_fc(self):
        return 'checked' if self.is_complete else ''

    def is_approved_fc(self):
        return 'checked' if self.is_mod_approved else ''

    def get_tile_color(self):
        color = ''
        if self.is_mod_approved:
            color = 'bg-green3'
        elif self.is_complete:
            color = 'bg-success-subtle'

        return color

    def get_tile_border(self):
        color = ''
        if self.is_mod_approved:
            color = 'border-green3'
        elif self.is_complete:
            color = 'border-success-subtle'
        else:
            color = 'border-red3'
        return color

    def get_check_mark_color(self):
        if self.is_mod_approved:
            color = 'color-green3'
        elif self.is_complete:
            color = 'color-accent'

        return color

    def get_url(self):
        if self.tile.img:
            return self.tile.img.url
        else:
            return ''


class SpecialTile(models.Model):
    # action
    pass
