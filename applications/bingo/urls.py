from django.urls import path

from applications.bingo.views import *

app_name = 'bingo'

urlpatterns = [
    path('create_bingo', CreateBingo.as_view(), name='create_bingo'),
    # path('edit_bingo/<int:pk>', EditBingo.as_view(), name='edit_bingo'),
    path('edit_bingo_board/<int:pk>', EditBingoBoard.as_view(), name='edit_bingo_board'),
    path('edit_bingo_players/<int:pk>', EditBingoPlayers.as_view(), name='edit_bingo_players'),
    path('edit_bingo_teams/<int:pk>', EditBingoTeams.as_view(), name='edit_bingo_teams'),
    path('edit_bingo_setting/<int:pk>', EditBingoSetting.as_view(), name='edit_bingo_setting'),

    path('delete_team/<int:pk>', DeleteTeam.as_view(), name='delete_team'),
    path('delete_board/<int:pk>', DeleteBoard.as_view(), name='delete_board'),

    path('launch_bingo/<int:pk>', LaunchBingo.as_view(), name='launch_bingo'),

    path('kick_bingo_player/<int:pk>/<int:player_pk>', KickPlayer.as_view(), name='kick_bingo_player'),

    path('change_team/<int:pk>', ChangeTeam.as_view(), name='change_team'),
    path('change_team_moderator/<int:pk>/<int:player_pk>', ChangeTeamModerator.as_view(), name='change_team_moderator'),
    path('create_team/<int:pk>', CreateTeam.as_view(), name='create_team'),

    path('join_bingo/<int:pk>', JoinBingo.as_view(), name='join_bingo'),
    path('actually_join_bingo/<int:pk>', ActuallyJoinBingo.as_view(), name='actually_join_bingo'),
    path('bingo_home_page/<int:pk>', BingoHomePage.as_view(), name='bingo_home_page'),

    path('play_bingo/<int:pk>/<int:team_pk>', PlayBingo.as_view(), name='play_bingo'),
    path('play_bingo/<int:pk>/', PlayBingoGeneral.as_view(), name='play_bingo_general'),
]
