from django.urls import path

from applications.tile.views import *

app_name = 'tile'

urlpatterns = [
    path('edit_tile/<uuid:pk>', EditTile.as_view(), name='edit_tile'),
    path('edit_invocation/<uuid:pk>', EditInvocation.as_view(), name='edit_invocation'),

    path('play_tile/<uuid:pk>', PlayTile.as_view(), name='play_tile'),
    path('complete_tile/<uuid:pk>', CompleteTile.as_view(), name='complete_tile'),
    path('approve_tile/<uuid:pk>', ApproveTile.as_view(), name='approve_tile')
]
