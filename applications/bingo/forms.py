from django import forms

from applications.bingo.models import Bingo


class BingoForm(forms.ModelForm):
    class Meta:
        model = Bingo
        fields = ['name', 'description', 'start_date', 'end_date', 'board_type', 'board_size', 'is_public',
                  'is_team_public', 'can_players_create_team', 'max_players_in_team', 'img']
        widgets = {
            'start_date': forms.DateTimeInput(),
            'end_date': forms.DateTimeInput(),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean(self):
        return super().clean()

    def is_valid(self):
        is_valid = super().is_valid()
        return is_valid


class EditBingoForm(forms.ModelForm):
    """
        Form used for editing the bingo
    """

    class Meta:
        model = Bingo
        exclude = ['is_ready', 'board_type', 'board_size', 'max_score']  # , 'is_over'

        widgets = {
            'start_date': forms.DateTimeInput(),
            'end_date': forms.DateTimeInput(),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }


class ModeratorForm(forms.Form):
    player_name = forms.CharField(
        max_length=32, required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
