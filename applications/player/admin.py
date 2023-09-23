from django.contrib import admin

# Register your models here.
from applications.player.models import Player, Moderator

admin.site.register(Player)
admin.site.register(Moderator)