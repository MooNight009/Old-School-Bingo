from django.contrib import admin

# Register your models here.
from applications.tile.models import Tile, TeamTile

admin.site.register(Tile)
admin.site.register(TeamTile)