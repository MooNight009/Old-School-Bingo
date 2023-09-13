import datetime

from django import forms

from applications.bingo.models import Bingo


class BingoForm(forms.ModelForm):
    class Meta:
        model = Bingo
        fields = ['name', 'description', 'start_date', 'end_date', 'board_type', 'board_size', 'is_public',
                  'is_team_public', 'can_players_create_team', 'max_players_in_team', 'img']
        widgets = {
            'start_date': forms.SelectDateWidget(),
            'end_date': forms.SelectDateWidget(),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean(self):
        clean = super(EditBingoForm, self).clean()

        # Make sure the new start date is not before today
        if clean['start_date'] <= datetime.datetime.now(datetime.timezone.utc):
            raise forms.ValidationError({'start_date': ['Start date has to be in the future']})
        elif clean['end_date'] <= clean['start_date']:
            raise forms.ValidationError({'end_date': ['How can you end what have not started']})

        return clean


class EditBingoForm(forms.ModelForm):
    """
        Form used for editing the bingo
    """

    class Meta:
        model = Bingo
        exclude = ['is_ready', 'board_type', 'board_size', 'max_score', 'is_started', 'is_over']
        labels = {
            'img': 'Bingo image'
        }

        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_game_over_on_finish': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_team_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_players_in_team': forms.NumberInput(attrs={'class': 'form-control'})
        }

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

        return clean

    def save(self, commit=True):
        super(EditBingoForm, self).save()


class ModeratorForm(forms.Form):
    player_name = forms.CharField(
        max_length=32, required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
