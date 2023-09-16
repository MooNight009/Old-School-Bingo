from django.db import models

from applications.tile.models import TeamTile


# from applications.player.models import Player


class Team(models.Model):
    team_name = models.CharField(max_length=64)
    score = models.IntegerField(default=0)
    ranking = models.IntegerField(default=1)

    bingo = models.ForeignKey('bingo.Bingo', on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        is_new = False
        if not self.pk:
            is_new = True
            if Team.objects.filter(bingo=self.bingo).order_by('-ranking').exists():
                self.ranking = Team.objects.filter(bingo=self.bingo).order_by('-ranking').first().ranking + 1
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if is_new:
            for tile in self.bingo.get_tiles():
                team_tile = TeamTile(team=self, tile=tile)
                team_tile.save()

    def delete(self, *args, **kwargs):
        if self.team_name == 'General':
            return ''

        for player in self.player_set.all():
            player.teams.remove(self)
            player.teams.add(Team.objects.get(bingo=self.bingo, team_name='General'))
            player.save()
        return super().delete(*args, **kwargs)

    def get_ranking(self):
        # ss = Team.objects.filter(bingo=self.bingo, score__gte=self.score).exclude(team_name='General').values('score')
        # return ss.distinct().count()
        return self.ranking

    def row_col_completion(self, team_tile):
        # If a row or column is completed add extra point
        board_size = self.bingo.board_size
        # Row
        starting_i = int((team_tile.tile.bingo_location - 1) / board_size) * board_size + 1
        row_range = [*range(starting_i, starting_i + board_size)]
        row_tiles = TeamTile.objects.filter(team=self, tile__bingo=team_tile.team.bingo,
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
