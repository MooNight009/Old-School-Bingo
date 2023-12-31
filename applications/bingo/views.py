# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import FormView, RedirectView, DetailView, ListView, UpdateView

from applications.bingo.forms import *
from applications.bingo.models import Bingo
from applications.common.mixins import UserIsModeratorMixin, PlayerAccessMixin
from applications.common.validators import check_string_special_free
from applications.player.models import Player, Moderator, PlayerBingoDetail
from applications.submission.models import Achievement, Submission
from applications.team.forms import TeamFormSet
from applications.team.models import Team
from applications.tile.models import Tile, TeamTile
from common.wiseoldman.wiseoldman import create_competition, update_team, delete_competition


class CreateBingo(LoginRequiredMixin, FormView):
    template_name = 'pages/bingo/create/create.html'
    form_class = BingoForm
    success_url = '/main'

    def form_valid(self, form):
        bingo = form.save()
        create_competition(bingo)
        player = Player.objects.filter(user=self.request.user).get()
        moderator = Moderator(player=player, bingo=bingo)
        moderator.save()
        for i in range(1, bingo.board_size ** 2 + 1):
            Tile.objects.create(bingo_location=i, score=1, bingo=bingo)

        bingo.calculate_max_score()
        Team.objects.create(team_name='General', bingo=bingo)
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
        players = Player.objects.filter(playerbingodetail__bingo_id=self.kwargs['pk'])
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
        return reverse('bingo:edit_bingo_moderators', kwargs={'pk': kwargs['pk']})


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
        if Moderator.objects.filter(player__user=self.request.user, bingo=bingo).exists():
            delete_competition(bingo)
            bingo.delete()
        return "/"


# TODO: Rename to DeleteBingoTeam
class DeleteTeam(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        team = Team.objects.filter(pk=kwargs['pk']).get()
        url = reverse('bingo:edit_bingo', kwargs={'pk': team.bingo.id})
        team.delete()
        return url


class JoinBingo(FormView):
    form_class = JoinBingoForm
    template_name = 'pages/bingo/view/join.html'

    def get_success_url(self):
        return reverse('bingo:bingo_home_page', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        bingo = Bingo.objects.filter(pk=self.kwargs['pk']).get()
        player = Player.objects.filter(user=self.request.user).get()
        player_details = PlayerBingoDetail.objects.get_or_create(player=player, bingo=bingo)

        if player_details[1]:
            player_details = player_details[0]
            player_details.account_names = self.request.POST['account_names']

            if 'team_id' in self.request.POST and len(self.request.POST['team_id']) > 0 and Team.objects.filter(
                    pk=self.request.POST['team_id']).exists():
                team = Team.objects.get(pk=self.request.POST['team_id'])
                if bingo.team_set.contains(team.get()) and not team.is_full():
                    player_details.team = team.get()
                else:
                    player_details.team = bingo.team_set.get(team_name='General')
            else:
                player_details.team = bingo.team_set.get(team_name='General')

            player_details.save()
        return super(JoinBingo, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(JoinBingo, self).get_context_data(**kwargs)
        bingo = Bingo.objects.get(id=self.kwargs['pk'])
        teams = Team.objects.filter(bingo=bingo).exclude(team_name='General')
        context['bingo'] = bingo
        context['teams'] = teams

        user = self.request.user
        if not user.is_anonymous:
            player = Player.objects.get(user=user)
            context['is_in_bingo'] = player.playerbingodetail_set.filter(bingo=bingo).exists()
        else:
            context['is_in_bingo'] = False

        return context


# TODO : Delete method
class ActuallyJoinBingo(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk']).get()
        player = Player.objects.filter(user=self.request.user).get()
        player_details = PlayerBingoDetail.objects.get_or_create(player=player, bingo=bingo)

        if player_details[1]:
            if not check_string_special_free(self.request.POST['account_names']):
                return reverse("bingo:bingo_home_page", kwargs={'pk': bingo.id})
            player_details = player_details[0]
            player_details.account_names = self.request.POST['account_names']

            if 'team_id' in self.request.POST and len(self.request.POST['team_id']) > 0 and Team.objects.filter(
                    pk=self.request.POST['team_id']).exists():
                team = Team.objects.filter(pk=self.request.POST['team_id'])
                if bingo.team_set.contains(team.get()):
                    player_details.team = team.get()
                else:
                    player_details.team = bingo.team_set.get(team_name='General')
            else:
                player_details.team = bingo.team_set.get(team_name='General')

            player_details.save()

        url = reverse("bingo:bingo_home_page", kwargs={'pk': bingo.id})
        return url


class BingoHomePage(DetailView):
    model = Bingo
    template_name_field = 'bingo'
    template_name = 'pages/bingo/view/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teams = Team.objects.filter(bingo=self.object).exclude(team_name='General')
        if self.object.is_team_public:
            teams = teams.order_by('-score')
        else:
            teams = teams.order_by('team_name')

        context['teams'] = teams

        context['players'] = Player.objects.filter(playerbingodetail__bingo=self.object)
        return context


class KickPlayer(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    """
        Redirect for kicking player from bingo
    """

    def get_redirect_url(self, *args, **kwargs):
        player = Player.objects.get(pk=self.kwargs['player_pk'])
        bingo = Bingo.objects.get(pk=self.kwargs['pk'])
        print(PlayerBingoDetail.objects.filter(player=player, bingo=bingo).delete())

        return reverse('bingo:edit_bingo_players', kwargs={'pk': self.kwargs['pk']})


# TODO: Move to team
class UpdatePlayerDetail(LoginRequiredMixin, UserIsModeratorMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk']).get()
        player = Player.objects.get(pk=kwargs['player_pk'])
        player_detail = PlayerBingoDetail.objects.get(player=player, bingo=bingo)

        if validate_name_list(self.request.POST['account_names']) is not None:
            return reverse('bingo:edit_bingo_players', kwargs={'pk': kwargs['pk']})

        # Make sure a team is selected and not empty
        if self.request.POST.get('team_id', False):
            team = Team.objects.filter(id=self.request.POST['team_id']).get()
            if not team.is_full():
                prev_team = player_detail.team
                player_detail.team = team

        player_detail.account_names = self.request.POST.get('account_names', '')
        player_detail.save()
        if player_detail.team is not None and player_detail.team.team_name != 'General':
            if prev_team:
                update_team(prev_team)
            update_team(team)

        return reverse('bingo:edit_bingo_players', kwargs={'pk': kwargs['pk']})


# TODO: Move to team
class ChangeTeam(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.get(pk=kwargs['pk'])
        if bingo.get_is_started() or not bingo.can_players_create_team:
            return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})
        team = Team.objects.get(pk=self.request.POST['selected_team_id'])

        player = Player.objects.get(user=self.request.user)
        player_bingo_details = player.playerbingodetail_set.filter(bingo=bingo).get()

        if bingo.max_players_in_team == 0 or bingo.max_players_in_team > team.get_player_count():
            older_team = player_bingo_details.team
            player_bingo_details.team = team
            player_bingo_details.save()

            update_team(older_team)
            update_team(team)

        return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})


# TODO: Move to team
class CreateTeam(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        bingo = Bingo.objects.filter(pk=kwargs['pk']).get()
        new_team_name = self.request.POST['new_team_name']

        if not check_string_special_free(new_team_name):
            return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})

        if bingo.get_is_started() or not bingo.can_players_create_team:
            return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})

        if not Team.objects.filter(bingo=bingo, team_name=new_team_name).exists():
            # Create new team
            team = Team(team_name=new_team_name, bingo=bingo)
            team.save()

            # Add user to team
            user = self.request.user
            player = Player.objects.filter(user=user).get()
            player_bingo_detail = player.playerbingodetail_set.filter(bingo=bingo).get()
            player_bingo_detail.team = team
            player_bingo_detail.save()

            # Update WOM
            print("We got to here")
            update_team(team)

        return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})


# View to see the actual bingo game
# TODO: Fix team selection
class PlayBingo(PlayerAccessMixin, DetailView):
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


class PlayBingoGeneral(UserPassesTestMixin, DetailView):
    model = Bingo
    template_name_field = 'bingo'
    template_name = 'pages/bingo/view/general.html'

    def test_func(self):
        bingo = Bingo.objects.get(pk=self.kwargs['pk'])

        return (bingo.is_team_public and bingo.is_started) or (
                    bingo.is_public and bingo.is_over) or Moderator.objects.filter(player__user=self.request.user,
                                                                                   bingo_id=self.kwargs['pk']).exists()

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
