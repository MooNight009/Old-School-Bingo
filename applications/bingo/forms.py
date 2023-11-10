import datetime

from discord import SyncWebhook
from django import forms

from applications.bingo.models import Bingo
from applications.common.validators import validate_string_special_free, validate_discord_link, validate_name_list
from applications.common.widgets import DateTimeWidget
from common.wiseoldman.wiseoldman import get_user


class BingoForm(forms.ModelForm):
    """
        This form is used when creating a bingo
        TODO: Update to include minimum required setting
    """

    class Meta:
        model = Bingo
        fields = ['name', 'description', 'img', 'start_date', 'end_date',
                  'board_size', 'max_players_in_team']
        exclude = ['is_ready', 'max_score', 'is_started', 'is_over', 'is_game_over_on_finish', 'is_row_col_extra',
                   'is_public', 'is_team_public', 'can_players_create_team']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-md-25'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-md-50'}),
            'img': forms.FileInput(attrs={'class': 'form-control w-md-25', 'required': 'required'}),

            'start_date': DateTimeWidget(attrs={'class': 'btn-default w-md-25 rounded-3'}),
            'end_date': DateTimeWidget(attrs={'class': 'btn-default w-md-25 rounded-3'}),

            'board_size': forms.NumberInput(attrs={'class': 'form-control w-md-25'}),
            'max_players_in_team': forms.NumberInput(attrs={'class': 'form-control w-25'}),
        }

    def clean(self):
        clean = super().clean()

        # Make sure the new start date is not before today
        if clean['start_date'] <= datetime.datetime.now(datetime.timezone.utc):
            raise forms.ValidationError({'start_date': ['Start date has to be in the future']})
        elif clean['end_date'] <= clean['start_date']:
            raise forms.ValidationError({'end_date': ['How can you end what have not started']})
        elif (clean['end_date'] - clean['start_date']).days > 60:
            raise forms.ValidationError({'end_date': ['Duration of the bingo has to be less than 30 days']})

        # # Ensure is_public isn't off and is_team_public on
        # if not clean['is_public'] and clean['is_team_public']:
        #     raise forms.ValidationError({'is_team_public': ['Previous option has to be enabled for this to be on.']})

        return clean

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_string_special_free(name)
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        validate_string_special_free(description)
        return description


class EditBingoForm(forms.ModelForm):
    """
        Form used for editing the bingo setting
    """

    class Meta:
        model = Bingo
        fields = ['name', 'description', 'img', 'start_date', 'end_date', 'is_game_over_on_finish',
                  'is_row_col_extra', 'can_players_create_team',
                  'max_players_in_team', 'is_public', 'is_team_public', 'is_started', 'is_over']
        exclude = ['is_ready', 'max_score', 'board_size', 'board_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-md-25'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-md-50'}),
            'img': forms.FileInput(attrs={'class': 'form-control w-md-25'}),

            'start_date': DateTimeWidget(attrs={'class': 'btn-default w-md-25 rounded-3'}),
            'end_date': DateTimeWidget(attrs={'class': 'btn-default w-md-25 rounded-3'}),
            'is_game_over_on_finish': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'is_row_col_extra': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_team_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'can_players_create_team': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_players_in_team': forms.NumberInput(attrs={'class': 'form-control w-md-25'}),
        }

        localized_fields = ['start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(EditBingoForm, self).__init__(*args, **kwargs)
        if self.instance.is_started:
            self.fields['start_date'].disabled = True

        if self.instance.is_over:
            self.fields['end_date'].disabled = True
            self.fields['name'].disabled = True
            self.fields['description'].disabled = True
            self.fields['img'].disabled = True
            self.fields['is_game_over_on_finish'].disabled = True
            self.fields['is_row_col_extra'].disabled = True
            self.fields['can_players_create_team'].disabled = True
            self.fields['max_players_in_team'].disabled = True

    def clean(self):
        clean = super(EditBingoForm, self).clean()


        # Disable changing start date if it's started
        # TODO: Disable the option to begin with
        if self.instance.get_is_started():
            clean['start_date'] = self.instance.start_date
        # Make sure the new start date is not before today
        elif clean['start_date'] <= datetime.datetime.now(datetime.timezone.utc):
            raise forms.ValidationError({'start_date': ['Start date has to be in the future']})
        elif clean['end_date'] <= clean['start_date']:
            raise forms.ValidationError({'end_date': ['How can you end what have not started']})
        elif (clean['end_date'] - clean['start_date']).days > 60:
            raise forms.ValidationError({'end_date': ['Duration of the bingo has to be less than 30 days']})


        # Ensure is_public isn't off and is_team_public on
        # if not clean['is_public'] and clean['is_team_public']:
        #     raise forms.ValidationError({'is_team_public': ['Previous option has to be enabled for this to be on.']})

        return clean

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_string_special_free(name)
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        print("We here")
        validate_string_special_free(description)
        print("But not here")
        return description


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
        cleaned_data = super(EditBingoDiscordForm, self).clean()
        if 'discord_webhook' not in cleaned_data:
            if 'discord_webhook' in self._errors:
                return cleaned_data

        if ('discord_webhook' in self.changed_data or 'enable_discord' in self.changed_data) and cleaned_data[
            'enable_discord']:
            try:
                webhook = SyncWebhook.from_url(cleaned_data['discord_webhook'])
                webhook.send(f'You are now connected to the bingo **{self.instance.name}** from Old School Bingo.')
            except ValueError:
                raise forms.ValidationError(
                    {'discord_webhook': [
                        'The webhook you entered is not working. Make sure to follow the documentation.']})

        return cleaned_data

    def clean_discord_webhook(self):
        discord_webhook = self.cleaned_data['discord_webhook']
        validate_discord_link(discord_webhook)
        return discord_webhook


class ModeratorForm(forms.Form):
    player_name = forms.CharField(
        max_length=32, validators=[validate_string_special_free], required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class JoinBingoForm(forms.Form):
    account_names = forms.CharField(
        max_length=128, validators=[validate_name_list], required=False,
        widget=forms.TextInput(attrs={'class': 'form-control w-md-50'}),
        help_text="For multiple accounts separate them by a ',"
                  "' (comma). This information will be used for tiles that get data from WiseOldMan.")

    def clean_account_names(self):
        account_names = self.cleaned_data['account_names']
        for account_name in account_names.split(','):
            if len(account_name) != 0:
                account = get_user(account_name)
                if account.status_code != 200 or account.status_code != 200:
                    raise forms.ValidationError([f'No account found with the name {account_name}. Make '
                                                 f'sure you typed the name correctly or leave the field empty'])

        return account_names
