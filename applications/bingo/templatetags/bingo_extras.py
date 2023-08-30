from django import template

from applications.bingo.models import Bingo
from applications.player.models import Player, Moderator
from applications.team.models import Team

register = template.Library()


@register.filter(name='is_user_in_team')
def is_user_in_team(user, team):
    player = Player.objects.filter(user=user).get()
    output = ''
    if player.teams.contains(team):
        output = 'selected'
    return output


@register.filter(name='is_player_in_team')
def is_player_in_team(player, team):
    # player = Player.objects.filter(user=user).get()
    output = ''
    if player.teams.contains(team):
        output = 'selected'
    return output


@register.filter(name='get_user_bingo_team')
def get_user_bingo_team(user, bingo):
    player = Player.objects.get(user=user)
    team_id = -1
    # Is the player in bingo
    if player.bingos.contains(bingo):
        team = player.teams.filter(bingo=bingo).exclude(team_name='General')
        if team.exists():
            team_id = team.get().id
    # Is the player a moderator
    elif Moderator.objects.filter(player=player, bingo=bingo):
        team = Team.objects.filter(bingo=bingo).first()
        if team is not None:
            team_id = team.id

    return team_id


@register.filter(name='get_player_bingo_team')
def get_player_bingo_team(player, bingo):
    # player = Player.objects.get(user=user)
    team_id = -1
    # Is the player in bingo
    if player.bingos.contains(bingo):
        team = player.teams.filter(bingo=bingo).exclude(team_name='General')
        if team.exists():
            team_id = team.get().id
    # Is the player a moderator
    elif Moderator.objects.filter(player=player, bingo=bingo):
        team = Team.objects.filter(bingo=bingo).first()
        if team is not None:
            team_id = team.id

    return team_id


@register.filter(name='get_user_bingo_id_team')
def get_user_bingo_id_team(user, bingo_pk):
    bingo = Bingo.objects.filter(pk=bingo_pk)
    player = Player.objects.filter(user=user).get()
    team_id = -1
    # Is the player in bingo
    if player.bingos.contains(bingo):
        team = player.teams.filter(bingo=bingo).get()
        team_id = team.id
    # Is the player a moderator
    elif Moderator.objects.filter(player=player, bingo=bingo):
        team = Team.objects.filter(bingo=bingo).first()
        if team is not None:
            team_id = team.id

    return team_id


@register.filter(name='user_access_check')
def user_access_check(user, team_pk):
    team = Team.objects.get(pk=team_pk)
    player = Player.objects.get(user=user)

    if not team.bingo.is_public and not Moderator.objects.filter(player=player, bingo=team.bingo):
        if not team.bingo.is_team_public:
            if not player.teams.contains(team):
                return 'disabled'

    return ''


@register.filter(name='is_moderator')
def is_moderator(user, bingo_pk):
    return Moderator.objects.filter(player__user=user, bingo_id=bingo_pk).exists()


@register.filter(name='get_player_bingo_team_name')
def get_player_bingo_team_name(player, bingo_pk):
    team_name = player.teams.get(bingo=bingo_pk).team_name

    return team_name if team_name!= 'General' else 'No team'

