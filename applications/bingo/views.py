# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import FormView, RedirectView, DetailView, ListView, UpdateView

from applications.bingo.forms import *
from applications.bingo.models import Bingo
from applications.common.mixins import UserIsModeratorMixin, PlayerAccessMixin
from applications.player.models import Player, Moderator, PlayerBingoDetail
from applications.submission.models import Achievement, Submission
from applications.team.forms import TeamFormSet
from applications.team.models import Team
from applications.tile.models import Tile, TeamTile


class CreateBingo(LoginRequiredMixin, FormView):
    template_name = 'pages/bingo/create/create.html'
    form_class = BingoForm
    success_url = '/'

    def form_valid(self, form):
        bingo = form.save()
        player = Player.objects.filter(user=self.request.user).get()
        moderator = Moderator(player=player, bingo=bingo)
        moderator.save()
        for i in range(1, bingo.board_size ** 2 + 1):
            tile = Tile(bingo_location=i, score=1,
                        bingo=bingo)
            tile.save()
        Team(team_name='General', bingo=bingo).save()
        return super().form_valid(form)


class EditBingoBoard(LoginRequiredMixin, UserIsModeratorMixin, DetailView):
    model = Bingo
    context_object_name = 'bingo'
    template_name = 'pages/bingo/edit/board.html'

    # def get_queryset(self):
    #     return self.model.objects.filter(tile__bingo=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class EditBingoTeams(LoginRequiredMixin, UserIsModeratorMixin, FormView):
    form_class = TeamFormSet
    template_name = 'pages/bingo/edit/teams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bingo = Bingo.objects.get(pk=self.kwargs['pk'])
        context['bingo'] = bingo

        return context

    def get_form(self, form_class=None):
        if self.request.POST:
            return TeamFormSet(self.request.POST, instance=Bingo.objects.get(pk=self.kwargs['pk']))
        return TeamFormSet(instance=Bingo.objects.get(pk=self.kwargs['pk']))

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("bingo:edit_bingo_teams", kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        for f in form:
            if len(f.cleaned_data) != 0:
                if f.cleaned_data['id'] is not None and f.cleaned_data['id'].team_name == 'General':
                    f.cleaned_data['team_name'] = 'General'
                    f.instance.team_name = 'General'

        form.save()
        return super().form_valid(form)


class EditBingoPlayers(LoginRequiredMixin, UserIsModeratorMixin, ListView):
    model = Player
    context_object_name = 'players'
    template_name = 'pages/bingo/edit/players.html'

    def get_queryset(self):
        players = Player.objects.filter(bingos__in=Bingo.objects.filter(pk=self.kwargs['pk']))
        return players

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        context['teams'] = Team.objects.filter(bingo_id=self.kwargs['pk'])
        context['bingo'] = Bingo.objects.filter(pk=self.kwargs['pk']).get()
        return context


class EditBingoModerators(LoginRequiredMixin, UserIsModeratorMixin, FormView):
    form_class = ModeratorForm
    template_name = 'pages/bingo/edit/moderators.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bingo'] = Bingo.objects.get(pk=self.kwargs['pk'])
        context['mods'] = Moderator.objects.filter(bingo_id=self.kwargs['pk'])

        return context

    def form_valid(self, form):
        player = Player.objects.filter(user__username=form.cleaned_data['player_name'])
        if player.exists():
            if not Moderator.objects.filter(player=player.get(), bingo_id=self.kwargs['pk']).exists():
                Moderator.objects.create(player=player.get(), bingo_id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bingo:edit_bingo_moderators', kwargs={'pk': self.kwargs['pk']})

class KickModerator(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if Moderator.objects.filter(bingo_id=kwargs['pk']).count() > 1:
            mod = Moderator.objects.get(pk=kwargs['mod_pk'])
            mod.delete()
        return reverse('bingo:edit_bingo_moderators', kwargs={'pk':kwargs['pk']})

class EditBingoSetting(LoginRequiredMixin, UserIsModeratorMixin, UpdateView):
    """
        Edit bingo details : Setting
    """
    model = Bingo
    context_object_name = 'bingo'
    form_class = EditBingoForm

    template_name = 'pages/bingo/edit/setting.html'

    def get_success_url(self):
        return reverse('bingo:edit_bingo_setting', kwargs={'pk': self.kwargs['pk']})


class EditBingoDiscord(LoginRequiredMixin, UserIsModeratorMixin, UpdateView):
    """
        Edit bingo details : Discord
    """
    model = Bingo
    context_object_name = 'bingo'
    form_class = EditBingoDiscordForm

    template_name = 'pages/bingo/edit/discord.html'

    def get_success_url(self):
        return reverse('bingo:edit_bingo_discord', kwargs={'pk': self.kwargs['pk']})

# Add delete confirmation later
# TODO: Switch name to DeleteBingo
class DeleteBoard(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk']).get()
        bingo.delete()
        print("Deleting board disabled")
        return "/"


# TODO: Rename to DeleteBingoTeam
class DeleteTeam(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        team = Team.objects.filter(pk=kwargs['pk']).get()
        url = reverse('bingo:edit_bingo', kwargs={'pk': team.bingo.id})
        team.delete()
        return url


class JoinBingo(DetailView):
    model = Bingo
    template_name = 'pages/bingo/view/join.html'

    def get_context_data(self, **kwargs):
        context = super(JoinBingo, self).get_context_data(**kwargs)
        teams = Team.objects.filter(bingo=self.object).exclude(team_name='General')
        context['teams'] = teams

        user = self.request.user
        if not user.is_anonymous:
            player = Player.objects.get(user=user)
            context['is_in_bingo'] = player.bingos.contains(self.object)
        else:
            context['is_in_bingo'] = False

        return context


class BingoHomePage(LoginRequiredMixin, DetailView):
    model = Bingo
    template_name_field = 'bingo'
    template_name = 'pages/bingo/view/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = Team.objects.filter(bingo=self.object).exclude(team_name='General').order_by('-score')
        context['teams'] = teams

        user = self.request.user
        player = Player.objects.get(user=user)
        context['is_in_bingo'] = player.bingos.contains(self.object)

        context['players'] = Player.objects.filter(bingos__in=[self.object])
        return context


class ActuallyJoinBingo(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk']).get()
        user = self.request.user
        player = Player.objects.filter(user=user).get()
        if not player.bingos.contains(bingo):
            player.bingos.add(bingo)
            player_details = PlayerBingoDetail.objects.get_or_create(player=player, bingo=bingo)[0]
            player_details.account_names = self.request.POST['account_names']
            player_details.save()

        player.teams.add(bingo.team_set.get(team_name='General'))

        url = reverse("bingo:bingo_home_page", kwargs={'pk': bingo.id})
        return url


class KickPlayer(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    """
        Redirect for kicking player from bingo
    """

    def get_redirect_url(self, *args, **kwargs):
        player = Player.objects.get(pk=self.kwargs['player_pk'])
        bingo = Bingo.objects.get(pk=self.kwargs['pk'])
        player.bingos.remove(bingo)
        player.teams.remove(*Team.objects.filter(bingo=bingo))

        return reverse('bingo:edit_bingo_players', kwargs={'pk': self.kwargs['pk']})


# TODO: Move to team
class ChangeTeamModerator(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk']).get()
        if self.request.POST.get('team_id', False):
            team = Team.objects.filter(pk=self.request.POST['team_id']).get()

            player = Player.objects.get(pk=kwargs['player_pk'])
            joined_teams = player.teams.filter(bingo=bingo)
            for joined_team in joined_teams:
                player.teams.remove(joined_team)
            player.teams.add(team)

        return reverse('bingo:edit_bingo_players', kwargs={'pk': kwargs['pk']})


# TODO: Move to team
class ChangeTeam(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.get(pk=kwargs['pk'])
        if bingo.get_is_started():
            return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})
        team = Team.objects.get(pk=self.request.POST['selected_team_id'])

        player = Player.objects.get(user=self.request.user)
        joined_teams = player.teams.filter(bingo=bingo)
        players_in_team_count = Player.objects.filter(teams__in=[team]).count()
        # TODO: Make sure this works as intended
        if bingo.max_players_in_team == 0 or bingo.max_players_in_team > players_in_team_count:
            for joined_team in joined_teams:
                player.teams.remove(joined_team)
            player.teams.add(team)
        return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})


# TODO: Move to team
class CreateTeam(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk']).get()
        new_team_name = self.request.POST['new_team_name']
        if bingo.get_is_started():
            return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})

        if not Team.objects.filter(bingo=bingo, team_name=new_team_name).exists():
            # Create new team
            team = Team(team_name=new_team_name, bingo=bingo)
            team.save()

            # Add user to team
            user = self.request.user
            player = Player.objects.filter(user=user).get()
            player.teams.remove(player.teams.get(bingo=bingo))
            player.teams.add(team)

        return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})


# View to see the actual bingo game
# TODO: Fix team selection
class PlayBingo(LoginRequiredMixin, PlayerAccessMixin, DetailView):
    model = Bingo
    access_object = 'bingo'
    template_name_field = 'bingo'
    template_name = 'pages/bingo/view/play.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(pk=self.kwargs['team_pk']).get()
        team_tiles = TeamTile.objects.filter(team=team).order_by('tile__bingo_location').all()
        context['team_tiles'] = team_tiles
        context['teams'] = Team.objects.filter(bingo=self.object).all()
        context['current_team'] = team
        context['achievements'] = Achievement.objects.filter(team_tile__in=team_tiles).order_by('-date')
        context['submissions'] = Submission.objects.filter(team_tile__in=team_tiles).order_by('-date')
        return context


class PlayBingoGeneral(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Bingo
    template_name_field = 'bingo'
    template_name = 'pages/bingo/view/general.html'

    def test_func(self):
        bingo = Bingo.objects.get(pk=self.kwargs['pk'])

        return Moderator.objects.filter(player__user=self.request.user,
                                        bingo_id=self.kwargs['pk']).exists() or (bingo.is_team_public and bingo.is_started)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team = Team.objects.get(team_name='General', bingo=context['bingo'])
        team_tiles = TeamTile.objects.filter(team=team).order_by('tile__bingo_location').all()
        context['team_tiles'] = team_tiles
        context['teams'] = Team.objects.filter(bingo=self.object).all()
        context['current_team'] = team
        context['achievements'] = Achievement.objects.filter(team_tile__team__bingo=context['bingo']).order_by('-date')
        context['submissions'] = Submission.objects.filter(team_tile__team__bingo=context['bingo']).order_by('-date')

        return context


# Not Implemented
class LaunchBingo(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk'].get())
        return '/'
