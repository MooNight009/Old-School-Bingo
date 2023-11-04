from discord import SyncWebhook
from django import forms

from applications.bingo.models import Bingo
# TODO: Write clean methods for each part
from applications.common.validators import validate_discord_link, validate_string_special_free
from applications.team.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'discord_webhook']

        widgets = {
            'team_name' : forms.TextInput(attrs={'class':'form-control w-25 me-2'}),
            'discord_webhook' : forms.TextInput(attrs={'class':'form-control w-25 me-2'})
        }

    def clean(self):
        cleaned_data = super().clean()
        if 'discord_webhook' not in cleaned_data or 'team_name' not in cleaned_data:
            if 'discord_webhook' in self._errors or 'team_name' in self._errors:
                return cleaned_data

        if Team.objects.filter(bingo=self.instance.bingo, team_name=cleaned_data['team_name']).exclude(
                id=self.instance.id).exists():
            raise forms.ValidationError({'team_name': ['Team name already exists']})

        try:
            if cleaned_data['discord_webhook']is not None and len(cleaned_data['discord_webhook'])!= 0:
                webhook = SyncWebhook.from_url(cleaned_data['discord_webhook'])
                webhook.send(f'You are now connected to team **{cleaned_data["id"].team_name}** in bingo **{cleaned_data["bingo"].name}** from OldSchoolBingo.')
        except ValueError:
            raise forms.ValidationError(
                {'discord_webhook': [
                    'The webhook you entered is not working. Make sure to the webhook is correct or leave empty if you do not want to use it.']})

        return cleaned_data

    def clean_team_name(self):
        team_name = self.cleaned_data['team_name']
        validate_string_special_free(team_name)
        return team_name

    def clean_discord_webhook(self):
        discord_webhook = self.cleaned_data['discord_webhook']
        if discord_webhook is not None:
            validate_discord_link(discord_webhook)
        return discord_webhook

TeamFormSet = forms.inlineformset_factory(Bingo, Team, form=TeamForm)
