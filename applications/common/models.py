import os

from django.db import models
from django.dispatch import receiver

from applications.bingo.models import Bingo
from applications.submission.models import Submission
from applications.tile.models import Tile


@receiver(models.signals.post_delete, sender=Tile)
@receiver(models.signals.post_delete, sender=Bingo)
@receiver(models.signals.post_delete, sender=Submission)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)


@receiver(models.signals.pre_save, sender=Tile)
@receiver(models.signals.pre_save, sender=Bingo)
@receiver(models.signals.pre_save, sender=Submission)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Tile.objects.get(pk=instance.pk).img
        if not old_file:
            return True
    except Tile.DoesNotExist:
        return False

    new_file = instance.img
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
