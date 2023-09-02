# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import FormView, RedirectView, DetailView, ListView, UpdateView

from applications.bingo.forms import BingoForm, EditBingoForm
from applications.bingo.models import Bingo
from applications.common.mixins import UserIsModeratorMixin, PlayerAccessMixin
from applications.player.models import Player, Moderator
from applications.submission.models import Achievement, Submission
from applications.team.forms import TeamFormSet
from applications.team.models import Team
from applications.tile.models import Tile, TeamTile


class CreateBingo(LoginRequiredMixin, FormView):
    template_name = 'pages/bingo/createbingo.html'
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


# class EditBingo(LoginRequiredMixin, UserIsModeratorMixin, FormView):
#     """
#         Page to edit the details of bingo
#         TODO: Switch to ModelForm or UpdateView
#         TODO: Split teams to another tab
#         TODO: Split settings to another tab
#     """
#     template_name = 'pages/bingo/edit/editbingo.html'
#     form_class = EditBingoForm
#     success_url = '/'
#
#     # Set the initial detail for the form
#     def get_initial(self):
#         initial = {'team_names': 'Bakasdojn'}
#         pk = self.kwargs.get('pk')
#         bingo = Bingo.objects.filter(pk=pk).get()
#         initial['is_public'] = bingo.is_public
#         initial['is_team_public'] = bingo.is_team_public
#         initial['start_date'] = bingo.start_date
#         initial['end_date'] = bingo.end_date
#         initial['can_players_create_team'] = bingo.can_players_create_team
#         initial['max_players_in_team'] = bingo.max_players_in_team
#         return initial
#
#     # Get the bingo object
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         pk = self.kwargs.get('pk')
#         bingo = Bingo.objects.filter(pk=pk).get()
#         teams = Team.objects.filter(bingo=bingo)
#         context['bingo'] = bingo
#         context['teams'] = teams
#         return context
#
#     # Don't leave page after saving
#     def form_valid(self, form):
#         pk = self.kwargs.get('pk')
#         bingo = Bingo.objects.filter(pk=pk).get()
#         bingo.is_team_public = form.cleaned_data.get('is_team_public')
#         bingo.is_public = form.cleaned_data.get('is_public')
#         bingo.start_date = form.cleaned_data.get('start_date')
#         bingo.end_date = form.cleaned_data.get('end_date')
#
#         bingo.max_players_in_team = form.cleaned_data.get('max_players_in_team')
#         bingo.can_players_create_team = form.cleaned_data.get('can_players_create_team')
#
#         for l in self.request.POST.lists():
#             # Update existing teams
#             if "update_team_name" in l[0]:
#                 team_id = l[0].split("update_team_name_")[1]
#                 team = Team.objects.filter(id=team_id).get()
#                 if team.team_name != l[1][0]:
#                     team.team_name = l[1][0]
#                     team.save()
#             # We have new teams
#             elif l[0] == 'team_name_new':
#                 new_teams = l[1]
#                 for new_team in new_teams:
#                     team = Team(team_name=new_team, bingo=bingo)
#                     team.save()
#
#                     # Create TeamTiles for team
#                     # TODO: Move to a better place
#                     for tile in bingo.get_tiles():
#                         team_tile = TeamTile(team=team, tile=tile)
#                         team_tile.save()
#
#         bingo.save()
#         return self.render_to_response(self.get_context_data(form=form))


class EditBingoBoard(LoginRequiredMixin, UserIsModeratorMixin, DetailView):
    model = Bingo
    context_object_name = 'bingo'
    template_name = 'pages/bingo/edit/editbingoboard.html'

    # def get_queryset(self):
    #     return self.model.objects.filter(tile__bingo=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class EditBingoTeams(LoginRequiredMixin, UserIsModeratorMixin, FormView):
    form_class = TeamFormSet
    template_name = 'pages/bingo/edit/editbingoteams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bingo = Bingo.objects.get(pk=self.kwargs['pk'])
        context['bingo'] = bingo
        # context['team_formset'] = TeamFormSet(instance=bingo)

        return context

    def get_form(self, form_class=None):
        if self.request.POST:
            return TeamFormSet(self.request.POST, instance=Bingo.objects.get(pk=self.kwargs['pk']))
        return TeamFormSet(instance=Bingo.objects.get(pk=self.kwargs['pk']))

    def form_invalid(self, form):
        print("Form is invalid")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("bingo:edit_bingo_teams", kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EditBingoPlayers(LoginRequiredMixin, UserIsModeratorMixin, ListView):
    model = Player
    context_object_name = 'players'
    template_name = 'pages/bingo/edit/editbingoplayers.html'

    def get_queryset(self):
        players = Player.objects.filter(bingos__in=Bingo.objects.filter(pk=self.kwargs['pk']))
        return players

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EditBingoPlayers, self).get_context_data(object_list=None, **kwargs)
        context['teams'] = Team.objects.filter(bingo_id=self.kwargs['pk'])
        context['bingo'] = Bingo.objects.filter(pk=self.kwargs['pk']).get()
        return context


class EditBingoSetting(LoginRequiredMixin, UserIsModeratorMixin, UpdateView):
    """
        Edit bingo details : Setting
    """
    model = Bingo
    context_object_name = 'bingo'
    form_class = EditBingoForm

    template_name = 'pages/bingo/edit/editbingosetting.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        print(context['bingo'].start_date)
        return context

    def get_success_url(self):
        return reverse('bingo:edit_bingo_setting', kwargs={'pk': self.kwargs['pk']})


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
    template_name = 'pages/bingo/joinbingo.html'

    def get_context_data(self, **kwargs):
        context = super(JoinBingo, self).get_context_data(**kwargs)
        teams = Team.objects.filter(bingo=self.object).exclude(team_name='General')
        context['teams'] = teams

        user = self.request.user
        player = Player.objects.filter(user=user).get()
        context['is_in_bingo'] = player.bingos.contains(self.object)

        return context

class BingoHomePage(LoginRequiredMixin, DetailView):
    model = Bingo
    template_name_field = 'bingo'
    template_name = 'pages/bingo/bingohomepage.html'

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

        url = reverse("bingo:join_bingo", kwargs={'pk': bingo.id})
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

        # Create new team
        team = Team(team_name=new_team_name, bingo=bingo)
        team.save()

        # Add user to team
        user = self.request.user
        player = Player.objects.filter(user=user).get()
        player.teams.remove(player.teams.get(bingo=bingo))
        player.teams.add(team)

        # Create TeamTiles for team
        # TODO: Move to a better place
        for tile in bingo.get_tiles():
            team_tile = TeamTile(team=team, tile=tile)
            team_tile.save()

        return reverse('bingo:bingo_home_page', kwargs={'pk': bingo.id})


# View to see the actual bingo game
# TODO: Fix team selection
class PlayBingo(PlayerAccessMixin, DetailView):
    model = Bingo
    access_object = 'bingo'
    template_name_field = 'bingo'
    template_name = 'pages/bingo/playbingo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(pk=self.kwargs['team_pk']).get()
        team_tiles = TeamTile.objects.filter(team=team).order_by('tile__bingo_location')
        context['team_tiles'] = team_tiles
        context['teams'] = Team.objects.filter(bingo=self.object).all()
        context['current_team'] = team
        context['achievements'] = Achievement.objects.filter(team_tile__in=team_tiles).order_by('-date')
        context['submissions'] = Submission.objects.filter(team_tile__in=team_tiles).order_by('-date')
        return context


class PlayBingoGeneral(UserPassesTestMixin, DetailView):
    model = Bingo
    template_name_field = 'bingo'
    template_name = 'pages/bingo/playbingogeneral.html'

    def test_func(self):
        return Moderator.objects.filter(player__user=self.request.user,
                                        bingo_id=self.kwargs['pk']).exists() or Bingo.objects.filter(
            pk=self.kwargs['pk']).get().is_team_public

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        team = Team.objects.get(team_name='General', bingo=context['bingo'])
        team_tiles = TeamTile.objects.filter(team=team)
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
