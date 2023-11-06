from django import template

from applications.bingo.models import Bingo
from applications.player.models import Player, Moderator, PlayerBingoDetail
from applications.team.models import Team

register = template.Library()


@register.filter(name='is_user_in_team')
def is_user_in_team(user, team):
    if user.is_anonymous:
        return ''
    player = Player.objects.get(user=user)
    output = ''
    if player.playerbingodetail_set.filter(team=team).exists():
        output = 'selected'
    return output


@register.filter(name='is_player_in_team')
def is_player_in_team(player, team):
    output = ''
    if player.playerbingodetail_set.filter(team=team).exists():
        output = 'selected'
    return output


@register.filter(name='get_user_bingo_team')
def get_user_bingo_team(user, bingo):
    if user.is_anonymous:
        return -1
    player = Player.objects.get(user=user)

    team_id = -1
    # Is the player in bingo
    player_detail = player.playerbingodetail_set.filter(bingo=bingo)
    if player_detail.exists():
        if player_detail.get().team.team_name != 'General':
            team_id = player_detail.get().team.id

    return team_id


@register.filter(name='get_player_bingo_team')
def get_player_bingo_team(player, bingo):
    # player = Player.objects.get(user=user)
    team_id = -1
    # Is the player in bingo
    player_detail = player.playerbingodetail_set.filter(bingo=bingo)
    if player_detail.exists():
        if player_detail.get().team.team_name != 'General':
            team_id = player_detail.get().team.id

    # Is the player a moderator
    # TODO: Better method than just calling the first team
    if team_id == -1 and Moderator.objects.filter(player=player, bingo=bingo):
        team = Team.objects.filter(bingo=bingo).first()
        if team is not None:
            team_id = team.id

    return team_id


@register.filter(name='get_user_bingo_id_team')
def get_user_bingo_id_team(user, bingo_pk):
    if user.is_anonymous:
        return -1

    bingo = Bingo.objects.get(id=bingo_pk)
    player = Player.objects.get(user=user)
    team_id = -1
    # Is the player in bingo
    player_detail = player.playerbingodetail_set.filter(bingo=bingo)
    if player_detail.exists():
        team_id = player_detail.get().team.id

    return team_id


@register.filter(name='user_access_check')
def user_access_check(user, team_pk):
    if user.is_anonymous:
        return ''
    team = Team.objects.get(pk=team_pk)
    player = Player.objects.get(user=user)

    if not Moderator.objects.filter(player=player, bingo=team.bingo):
        if not team.bingo.is_team_public:
            if not player.playerbingodetail_set.filter(team=team).exists():
                return 'disabled'

    return ''


@register.filter(name='is_moderator')
def is_moderator(user, bingo_pk):
    if user.is_anonymous:
        return False
    return Moderator.objects.filter(player__user=user, bingo_id=bingo_pk).exists()


@register.filter(name='get_player_bingo_team_name')
def get_player_bingo_team_name(player, bingo_pk):
    # team_name = player.teams.get(bingo_id=bingo_pk).team_name
    team_name = player.playerbingodetail_set.filter(bingo_id=bingo_pk).get().team.team_name

    return team_name if team_name != 'General' else 'No team'


# New filters
@register.filter(name='get_player_bingo_detail')
def get_player_bingo_detail(player, bingo):
    player_bingo_detail = PlayerBingoDetail.objects.filter(player=player, bingo=bingo)
    return None if not player_bingo_detail.exists() else player_bingo_detail.get()

@register.filter(name='get_user_bingo_detail')
def get_user_bingo_detail(user, bingo):
    if user.is_anonymous:
        return None
    player_bingo_detail = PlayerBingoDetail.objects.filter(player__user=user, bingo=bingo)
    return None if not player_bingo_detail.exists() else player_bingo_detail.get()
