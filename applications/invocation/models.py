import datetime
from abc import abstractmethod

import requests
from django.contrib.contenttypes.models import ContentType
from django.db import models

from applications.submission.models import Achievement


class Invocation(models.Model):
    tile = models.OneToOneField('tile.Tile', on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True

    @abstractmethod
    def update_complete(self, team_tile):
        pass

    @abstractmethod
    def update_approve(self, team_tile, username=None):
        bingo = self.tile.bingo
        team_tile.is_mod_approved = not team_tile.is_mod_approved

        if bingo.notify_approval:
            bingo.send_discord_message(
                f'Moderator **{username}** set the status of **{team_tile.tile.name}** approval to **{team_tile.is_complete}**.')

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
            team_tile.team.row_col_completion(team_tile)
            team_tile.team.save()
        team_tile.team.calculate_ranking(team_tile.team.bingo)

        # Finish the game
        if bingo.is_game_over_on_finish:
            if team_tile.team.score == bingo.max_score:
                bingo.is_over = True
                bingo.save()

        team_tile.save()


class SubmissionInvo(Invocation):

    def update_complete(self, team_tile, username):
        team_tile.is_complete = not team_tile.is_complete
        bingo = self.tile.bingo

        if bingo.notify_completion:
            bingo.send_discord_message(
                f'Player **{username}** set the status of **{team_tile.tile.name}** completion to **{team_tile.is_complete}**.')

        if team_tile.is_complete:
            team_tile.completion_date = datetime.datetime.now(datetime.timezone.utc)

        team_tile.save()



class WOMInvo(Invocation):
    TYPES = [
        ('XP', 'Experience'),
        ('KC', 'Bossing'),
        ('LV', 'Levels')
    ]

    type = models.CharField(max_length=2, default='LV', choices=TYPES)
    amount = models.IntegerField(default=1)
    names = models.CharField(max_length=256, default='overall',
                             help_text='Name of skills or bosses to track. "overall" for all. Separate by comma')


    def update_complete(self, team_tile, username):
        bingo = self.tile.bingo

        # Update wom details
        players_details = bingo.playerbingodetail_set.all().filter(team=team_tile.team)
        current_amount = 0
        for players_detail in players_details:
            names = players_detail.account_names.split(',')
            for name in names:
                update = requests.post(f'https://api.wiseoldman.net/v2/players/{name}/')
                # if update.status_code != 200:
                #     print(update.json())
                #     print("We got an error in player " + name)

                response = requests.get(
                    f'https://api.wiseoldman.net/v2/players/{name}/gained?startDate={bingo.start_date.strftime("%Y-%m-%dT%H:%M:%S")}&endDate={datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")}')
                type_names = self.names.split(',')
                if response.status_code == 200:
                    if self.type == 'KC':
                        for type_name in type_names:
                            current_amount += int(response.json()['data']['bosses'][type_name]['kills']['gained'])
                    elif self.type == 'XP':
                        for type_name in type_names:
                            current_amount += int(response.json()['data']['skills'][type_name]['experience']['gained'])
                    elif self.type == 'LV':
                        for type_name in type_names:
                            current_amount += int(response.json()['data']['bosses'][type_name]['level']['gained'])
                else:
                    print(response.json())

        team_tile.score = current_amount
        if current_amount >= self.amount:
            team_tile.is_complete = True

        if bingo.notify_completion:
            bingo.send_discord_message(
                f'Player **{username}** refreshed **{team_tile.tile.name}** to achieve **{current_amount}**/{self.amount}.')
        #
        if team_tile.is_complete:
            team_tile.completion_date = datetime.datetime.now(datetime.timezone.utc)
            self.update_approve(team_tile, username)
            team_tile.is_mod_approved = True


        team_tile.save()


BOSSES = ['abyssal_sire', 'alchemical_hydra', 'artio', 'barrows_chests', 'bryophyta', 'callisto', 'calvarion',
          'cerberus', 'chambers_of_xeric', 'chambers_of_xeric_challenge_mode', 'chaos_elemental', 'chaos_fanatic',
          'commander_zilyana', 'corporeal_beast', 'crazy_archaeologist', 'dagannoth_prime', 'dagannoth_rex',
          'dagannoth_supreme', 'deranged_archaeologist', 'duke_sucellus', 'general_graardor', 'giant_mole',
          'grotesque_guardians', 'hespori', 'kalphite_queen', 'king_black_dragon', 'kraken', 'kreearra',
          'kril_tsutsaroth', 'mimic', 'nex', 'nightmare', 'phosanis_nightmare', 'obor', 'phantom_muspah', 'sarachnis',
          'scorpia', 'skotizo', 'spindel', 'tempoross', 'the_gauntlet', 'the_corrupted_gauntlet', 'the_leviathan',
          'the_whisperer', 'theatre_of_blood', 'theatre_of_blood_hard_mode', 'thermonuclear_smoke_devil',
          'tombs_of_amascut', 'tombs_of_amascut_expert', 'tzkal_zuk', 'tztok_jad', 'vardorvis', 'venenatis', 'vetion',
          'vorkath', 'wintertodt', 'zalcano', 'zulrah']

SKILLS = ['overall', 'attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic', 'cooking',
          'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing', 'mining', 'herblore', 'agility',
          'thieving', 'slayer', 'farming', 'runecrafting', 'hunter', 'construction']
