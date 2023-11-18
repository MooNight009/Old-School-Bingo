from django.contrib import admin

# Register your models here.
from applications.tile.models import TileImage

admin.site.register(TileImage)