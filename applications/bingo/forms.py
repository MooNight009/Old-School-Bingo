from django import forms

from applications.bingo.models import Bingo


# TODO: Write clean methods for each part


class BingoForm(forms.ModelForm):
    class Meta:
        model = Bingo
        fields = ['name', 'description', 'start_date', 'end_date', 'board_type', 'board_size', 'is_public',
                  'is_team_public', 'can_players_create_team', 'max_players_in_team', 'img']
        widgets = {
            'start_date': forms.DateTimeInput(),
            'end_date': forms.DateTimeInput(),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }

    def clean(self):
        return super().clean()

    def is_valid(self):
        is_valid = super().is_valid()
        return is_valid


class EditBingoForm2(forms.Form):
    """
        A form to edit the bingo after creating it
        TODO: Fill the information here
        TODO: Use ModelForm
    """
    is_public = forms.BooleanField(label='is_public', required=False)
    is_team_public = forms.BooleanField(label='is_team_public', required=False)
    start_date = forms.DateTimeField(label='start_date', widget=forms.SelectDateWidget())
    end_date = forms.DateTimeField(label='end_date', widget=forms.SelectDateWidget())

    can_players_create_team = forms.BooleanField(label='can_players_create_bingo', required=False)
    max_players_in_team = forms.IntegerField()


class EditBingoForm(forms.ModelForm):
    """
        Form used for editting the bingo
    """

    class Meta:
        model = Bingo
        exclude = ['is_ready', 'board_type', 'board_size', 'max_score']  # , 'is_over'

        widgets = {
            'start_date': forms.DateTimeInput(),
            'end_date': forms.DateTimeInput(),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }

    # def __init__(self, *args, **kwargs):
    #     super(EditBingoForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({'class':'form-control'})


class ModeratorForm(forms.Form):
    player_name = forms.CharField(max_length=32, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
