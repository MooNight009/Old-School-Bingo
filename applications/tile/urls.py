from django.urls import path

from applications.tile.views import *

app_name= 'tile'

urlpatterns = [
    path('edit_tile/<int:pk>', EditTile.as_view(), name='edit_tile'),
    path('play_tile/<int:pk>', PlayTile.as_view(), name='play_tile'),
    path('complete_tile/<int:pk>', CompleteTile.as_view(), name='complete_tile'),
    path('approve_tile/<int:pk>', ApproveTile.as_view(), name='approve_tile')
]