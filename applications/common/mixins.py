from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse

from applications.bingo.models import Bingo
from applications.player.models import Player, Moderator
from applications.team.models import Team
from applications.tile.models import TeamTile


class UserIsModeratorMixin(UserPassesTestMixin):
    """
        Check whether the user is a moderator in this particular bingo
    """

    def test_func(self):
        return Moderator.objects.filter(bingo_id=self.kwargs['pk'], player__user=self.request.user).exists()


class PlayerAccessMixin(UserPassesTestMixin):
    """
        Check whether the user has access to the page
        access_object : determines how to find the bingo object
    """
    access_object = None
    bingo = None
    team = None
    player = None

    def test_func(self):
        # Get player object
        if not self.request.user.is_anonymous:
            player = Player.objects.get(user=self.request.user)

        # Get bingo object
        if self.access_object is None:
            return False
        elif self.access_object == 'bingo':
            bingo = Bingo.objects.get(pk=self.kwargs['pk'])
            if self.team is None:
                self.team = Team.objects.get(pk=self.kwargs['team_pk'])

            if not bingo.is_started and not Moderator.objects.filter(player=player, bingo=bingo).exists():
                return False
        elif self.access_object == 'team_tile':
            team_tile = TeamTile.objects.get(pk=self.kwargs['pk'])
            self.team = team_tile.team
            bingo = self.team.bingo

            if not bingo.is_started and not Moderator.objects.filter(player=player, bingo=bingo).exists():
                return False

        if bingo.is_public:
            return True
        elif player is not None:
            if player.bingos.contains(bingo) and not Moderator.objects.filter(bingo=bingo, player=player).exists():
                if bingo.is_team_public:
                    return True
                elif player.teams.contains(self.team):
                    return True
            elif Moderator.objects.filter(bingo=bingo, player=player).exists():
                return True

        return False
