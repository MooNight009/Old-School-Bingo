from django.contrib import admin

# Register your models here.
from applications.tile.models import Tile, TeamTile, TileImage

admin.site.register(Tile)
admin.site.register(TeamTile)
admin.site.register(TileImage)
