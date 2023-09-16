import datetime

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import UpdateView, RedirectView, CreateView

from applications.common.mixins import PlayerAccessMixin
from applications.invocation.forms import EditWOSInvoForm
from applications.invocation.models import SubmissionInvo, WOMInvo
from applications.player.models import Player, Moderator
from applications.submission.forms import SubmissionForm
from applications.submission.models import Submission, Achievement
from applications.team.models import Team
from applications.tile.forms import EditTileForm
from applications.tile.models import Tile, TeamTile


class EditTile(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'pages/tile/edit/edit.html'
    model = Tile
    context_object_name = 'tile'
    form_class = EditTileForm

    def test_func(self):
        return Moderator.objects.filter(bingo__tile=self.kwargs['pk'], player__user=self.request.user).exists()

    def form_valid(self, form):
        if form.has_changed() and form.instance.description != Tile().description and form.instance.name != Tile().name:
            form.instance.is_ready = True
            form.instance.bingo.calculate_max_score()

        # Create new invocation
        if 'invocation_type' in form.changed_data:
            self.object.invocation.delete()
            if form.cleaned_data['invocation_type'] == 'SBM':
                self.object.invocation = SubmissionInvo.objects.create(tile=self.object)
            elif form.cleaned_data['invocation_type'] == 'WOM':
                self.object.invocation = WOMInvo.objects.create(tile=self.object)

        return super(EditTile, self).form_valid(form)

    def get_success_url(self):
        return reverse('bingo:edit_bingo_board', kwargs={'pk': self.object.bingo.id})


class EditInvocation(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'pages/tile/edit/invocation.html'
    model = Tile
    context_object_name = 'tile'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, "object"):
            kwargs.update({"instance": self.object.invocation})
        return kwargs

    def get_form_class(self):
        if self.object.invocation_type == 'SBM':
            pass
        elif self.object.invocation_type == 'WOM':
            return EditWOSInvoForm

    def test_func(self):
        return Moderator.objects.filter(bingo__tile=self.kwargs['pk'], player__user=self.request.user).exists()

    def get_success_url(self):
        return reverse('tile:edit_tile', kwargs={'pk': self.object.tile.id})


class PlayTile(LoginRequiredMixin, PlayerAccessMixin, CreateView):
    """

    """
    model = Submission
    access_object = 'team_tile'
    form_class = SubmissionForm
    template_name = 'pages/tile/view/play.html'

    def get_context_data(self, **kwargs):
        """ Add to context:
            teamtile
            submissions"""
        context = super().get_context_data(**kwargs)
        context['teamtile'] = TeamTile.objects.filter(pk=self.kwargs['pk']).get()
        context['submissions'] = Submission.objects.filter(team_tile=context['teamtile']).all()
        return context

    def form_valid(self, form):
        """
            Add Player and TeamTile to the submission
        """
        player = Player.objects.get(user=self.request.user)
        form.instance.player = player
        team_tile = TeamTile.objects.get(pk=self.kwargs['pk'])
        form.instance.team_tile = team_tile

        if not (player.bingos.contains(team_tile.team.bingo) and player.teams.contains(
                team_tile.team)) and not Moderator.objects.filter(bingo=team_tile.team.bingo, player=player).exists():
            return super(PlayTile, self).form_invalid(form)
        if team_tile.tile.bingo.get_is_over() and not team_tile.tile.bingo.get_is_started():
            return super(PlayTile, self).form_invalid(form)

        return super(PlayTile, self).form_valid(form)

    def get_success_url(self):
        """Return to the same page after submission"""
        return reverse('tile:play_tile', kwargs={'pk': self.kwargs['pk']})


class CompleteTile(LoginRequiredMixin, PlayerAccessMixin, RedirectView):
    access_object = 'team_tile'

    def get_redirect_url(self, *args, **kwargs):
        team_tile = TeamTile.objects.get(pk=kwargs['pk'])

        bingo = team_tile.tile.bingo
        if bingo.get_is_over() or not bingo.get_is_started():
            return reverse('tile:play_tile', kwargs={'pk': team_tile.id})

        # Make the player is mod or part of team
        player = Player.objects.get(user=self.request.user)
        if not (player.bingos.contains(bingo) and player.teams.contains(
                team_tile.team) and not team_tile.is_complete) and not Moderator.objects.filter(bingo=bingo,
                                                                                                player=player).exists():
            return reverse('tile:play_tile', kwargs={'pk': team_tile.id})

        # Update tile completion
        team_tile.tile.invocation.update_complete(team_tile, self.request.user.username)

        return reverse('tile:play_tile', kwargs={'pk': team_tile.id})


class ApproveTile(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        team_tile = TeamTile.objects.filter(pk=kwargs['pk']).get()
        bingo = team_tile.tile.bingo
        if bingo.get_is_over() or not bingo.get_is_started():
            return reverse('tile:play_tile', kwargs={'pk': team_tile.id})

        # self.team_tile = team_tile
        if not Moderator.objects.filter(bingo=bingo, player__user=self.request.user).exists():
            return reverse('tile:play_tile', kwargs={'pk': team_tile.id})

        team_tile.tile.invocation.update_approve(team_tile, self.request.user.username)

        if team_tile.is_mod_approved:
            team_tile.team.score += team_tile.tile.score  # Add a point for finishing the tile

            team_tile.mod_approval_date = datetime.datetime.now(datetime.timezone.utc)
            achievement = Achievement(team_tile=team_tile)
            achievement.save()
        else:
            team_tile.team.score -= team_tile.tile.score  # Remove a point for unfinishing the tile

            achievement = Achievement.objects.filter(team_tile=team_tile)
            if achievement.exists():
                achievement.delete()

        team_tile.save()
        # Check if completing a row or column provides extra points.
        if team_tile.tile.bingo.is_row_col_extra:
            self.row_col_completion(team_tile)
            team_tile.team.save()
        self.calculate_ranking(team_tile.team.bingo)

        # Finish the game
        if bingo.is_game_over_on_finish:
            if team_tile.team.score == bingo.max_score:
                bingo.is_over = True
                bingo.save()

        return reverse('tile:play_tile', kwargs={'pk': team_tile.pk})

    def row_col_completion(self, team_tile):
        # If a row or column is completed add extra point
        board_size = team_tile.tile.bingo.board_size
        # Row
        starting_i = int((team_tile.tile.bingo_location - 1) / board_size) * board_size + 1
        row_range = [*range(starting_i, starting_i + board_size)]
        row_tiles = TeamTile.objects.filter(team=team_tile.team, tile__bingo=team_tile.team.bingo,
                                            tile__bingo_location__in=row_range).exclude(pk=team_tile.pk)
        # Col
        starting_j = int((team_tile.tile.bingo_location - 1) % board_size) + 1
        col_range = [*range(starting_j, board_size * board_size + 1, board_size)]
        col_tiles = TeamTile.objects.filter(team=team_tile.team, tile__bingo=team_tile.team.bingo,
                                            tile__bingo_location__in=col_range).exclude(pk=team_tile.pk)

        if not row_tiles.filter(is_mod_approved=False).exists():
            if team_tile.is_mod_approved:
                team_tile.team.score += 1;
            else:
                team_tile.team.score -= 1;

        if not col_tiles.filter(is_mod_approved=False).exists():
            if team_tile.is_mod_approved:
                team_tile.team.score += 1;
            else:
                team_tile.team.score -= 1;

    def calculate_ranking(self, bingo):
        teams = Team.objects.filter(bingo=bingo).exclude(team_name='General').all()
        scores = teams.values('score').distinct().order_by('-score')
        current_rank = 1
        for score in scores:
            tmp_teams = teams.filter(score=score['score'])
            for team in tmp_teams:
                team.ranking = current_rank
                team.save()
            current_rank += tmp_teams.count()
