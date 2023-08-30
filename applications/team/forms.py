from django import forms

from applications.bingo.models import Bingo


# TODO: Write clean methods for each part
from applications.team.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name']


TeamFormSet = forms.inlineformset_factory(Bingo, Team, form=TeamForm)