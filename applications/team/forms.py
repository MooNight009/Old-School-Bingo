from discord import SyncWebhook
from django import forms

from applications.bingo.models import Bingo
# TODO: Write clean methods for each part
from applications.team.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'discord_webhook']

    def clean(self):
        cleaned_data = super().clean()
        print('cleaned data')
        print(cleaned_data)
        print(cleaned_data['discord_webhook'])

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


TeamFormSet = forms.inlineformset_factory(Bingo, Team, form=TeamForm)
