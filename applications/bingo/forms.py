import datetime

from discord import SyncWebhook
from django import forms

from applications.bingo.models import Bingo
from applications.common.widgets import DateTimeWidget


class BingoForm(forms.ModelForm):
    class Meta:
        model = Bingo
        fields = ['name', 'description', 'img', 'start_date', 'end_date', 'is_game_over_on_finish', 'board_type',
                  'board_size', 'is_row_col_extra', 'is_public', 'is_team_public', 'can_players_create_team',
                  'max_players_in_team']
        exclude = ['is_ready', 'max_score', 'is_started', 'is_over']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-25'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-50'}),
            'img': forms.FileInput(attrs={'class': 'form-control w-25', 'required': 'required'}),

            # 'start_date': forms.SelectDateWidget(),
            'start_date': DateTimeWidget(attrs={'class': 'btn-default rounded-3'}),
            'end_date': DateTimeWidget(attrs={'class': 'btn-default rounded-3'}),
            'is_game_over_on_finish': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'board_size': forms.NumberInput(attrs={'class': 'form-control w-25'}),
            'board_type': forms.Select(attrs={'class': 'btn-default rounded-3'}),
            'is_row_col_extra': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_team_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'can_players_create_team': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_players_in_team': forms.NumberInput(attrs={'class': 'form-control w-25'}),
        }

    def clean(self):
        clean = super().clean()

        # Make sure the new start date is not before today
        if clean['start_date'] <= datetime.datetime.now(datetime.timezone.utc):
            raise forms.ValidationError({'start_date': ['Start date has to be in the future']})
        elif clean['end_date'] <= clean['start_date']:
            raise forms.ValidationError({'end_date': ['How can you end what have not started']})

        # Ensure is_public isn't off and is_team_public on
        if not clean['is_public'] and clean['is_team_public']:
            raise forms.ValidationError({'is_team_public': ['Previous option has to be enabled for this to be on.']})

        return clean


class EditBingoForm(forms.ModelForm):
    """
        Form used for editing the bingo
    """

    class Meta:
        model = Bingo
        fields = ['name', 'description', 'img', 'start_date', 'end_date', 'is_game_over_on_finish',
                  'is_row_col_extra', 'is_public', 'is_team_public', 'can_players_create_team',
                  'max_players_in_team']
        exclude = ['is_ready', 'max_score', 'board_size', 'board_type', 'is_started', 'is_over']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-25'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-50'}),
            'img': forms.FileInput(attrs={'class': 'form-control w-25'}),

            # 'start_date': forms.SelectDateWidget(),
            'start_date': DateTimeWidget(attrs={'class': 'btn-default rounded-3'}),
            'end_date': DateTimeWidget(attrs={'class': 'btn-default rounded-3'}),
            'is_game_over_on_finish': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'is_row_col_extra': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_team_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'can_players_create_team': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_players_in_team': forms.NumberInput(attrs={'class': 'form-control w-25'}),
        }

        localized_fields = ['start_date', 'end_date']
        

    def clean(self):
        clean = super(EditBingoForm, self).clean()

        if self.instance.get_is_over():
            raise forms.ValidationError('Bingo is over. You can not change anything anymore.')

        # Disable changing start date if it's started
        # TODO: Disable the option to begin with
        if self.instance.get_is_started():
            clean['start_date'] = self.instance.start_date
        # Make sure the new start date is not before today
        elif clean['start_date'] <= datetime.datetime.now(datetime.timezone.utc):
            raise forms.ValidationError({'start_date': ['Start date has to be in the future']})
        elif clean['end_date'] <= clean['start_date']:
            raise forms.ValidationError({'end_date': ['How can you end what have not started']})

        # Ensure is_public isn't off and is_team_public on
        if not clean['is_public'] and clean['is_team_public']:
            raise forms.ValidationError({'is_team_public': ['Previous option has to be enabled for this to be on.']})

        return clean


class EditBingoDiscordForm(forms.ModelForm):
    class Meta:
        model = Bingo
        fields = ['enable_discord', 'discord_webhook', 'notify_submission', 'notify_completion', 'notify_approval']

        labels = {
            'enable_discord': 'enable discord integration'
        }
        widgets = {
            'enable_discord': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'discord_webhook': forms.TextInput(attrs={'class': 'form-control w-25'}),
            'notify_submission': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_completion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_approval': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        if ('discord_webhook' in self.changed_data or 'enable_discord' in self.changed_data) and cleaned_data['enable_discord']:
            try:
                webhook = SyncWebhook.from_url(cleaned_data['discord_webhook'])
                webhook.send(f'You are now connected to the bingo **{self.instance.name}** from OldSchoolBingo.')
            except ValueError:
                raise forms.ValidationError(
                    {'discord_webhook': ['The webhook you entered is not working. Make sure to follow the documentation.']})

        return cleaned_data


class ModeratorForm(forms.Form):
    player_name = forms.CharField(
        max_length=32, required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
