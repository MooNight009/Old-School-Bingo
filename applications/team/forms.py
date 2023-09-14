from django import forms

from applications.bingo.models import Bingo
# TODO: Write clean methods for each part
from applications.team.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']

    def clean(self):
        cleaned_data = super().clean()

        if Team.objects.filter(bingo=self.instance.bingo, team_name=cleaned_data['team_name']).exclude(id=self.instance.id).exists():
            raise forms.ValidationError({'team_name':['Team name already exists']})

        return cleaned_data

TeamFormSet = forms.inlineformset_factory(Bingo, Team, form=TeamForm)
