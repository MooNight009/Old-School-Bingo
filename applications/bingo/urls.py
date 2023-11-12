from django.urls import path

from applications.bingo.views import *

app_name = 'bingo'

urlpatterns = [
    path('create_bingo', CreateBingo.as_view(), name='create_bingo'),
    # path('edit_bingo/<int:pk>', EditBingo.as_view(), name='edit_bingo'),
    path('edit_bingo_board/<uuid:pk>', EditBingoBoard.as_view(), name='edit_bingo_board'),
    path('edit_bingo_players/<uuid:pk>', EditBingoPlayers.as_view(), name='edit_bingo_players'),
    path('edit_bingo_teams/<uuid:pk>', EditBingoTeams.as_view(), name='edit_bingo_teams'),
    path('edit_bingo_setting/<uuid:pk>', EditBingoSetting.as_view(), name='edit_bingo_setting'),
    path('edit_bingo_discord/<uuid:pk>', EditBingoDiscord.as_view(), name='edit_bingo_discord'),
    path('edit_bingo_moderators/<uuid:pk>', EditBingoModerators.as_view(), name='edit_bingo_moderators'),
    path('kick_moderator/<uuid:pk>/<uuid:mod_pk>', KickModerator.as_view(), name='kick_moderator'),

    path('delete_team/<uuid:pk>', DeleteTeam.as_view(), name='delete_team'),
    path('delete_board/<uuid:pk>', DeleteBoard.as_view(), name='delete_board'),

    path('launch_bingo/<uuid:pk>', LaunchBingo.as_view(), name='launch_bingo'),

    path('kick_bingo_player/<uuid:pk>/<uuid:player_pk>', KickPlayer.as_view(), name='kick_bingo_player'),

    path('change_team/<uuid:pk>', ChangeTeam.as_view(), name='change_team'),
    path('update_player_detail/<uuid:pk>/<uuid:player_pk>', UpdatePlayerDetail.as_view(), name='update_player_detail'),
    path('create_team/<uuid:pk>', CreateTeam.as_view(), name='create_team'),

    path('join_bingo/<uuid:pk>', JoinBingo.as_view(), name='join_bingo'),
    path('actually_join_bingo/<uuid:pk>', ActuallyJoinBingo.as_view(), name='actually_join_bingo'),
    path('bingo_home_page/<uuid:pk>', BingoHomePage.as_view(), name='bingo_home_page'),

    path('play_bingo/<uuid:pk>/<uuid:team_pk>', PlayBingo.as_view(), name='play_bingo'),
    path('play_bingo/<uuid:pk>/', PlayBingoGeneral.as_view(), name='play_bingo_general'),
]
