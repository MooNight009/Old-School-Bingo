from django import forms

from applications.tile.models import Tile


class TileForm(forms.ModelForm):
    class Meta:
        model = Tile
        fields = ['name', 'description']


class EditTileForm(forms.ModelForm):
    class Meta:
        model = Tile
        fields = ['name', 'description', 'img', 'score']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'img': forms.FileInput(attrs={'class':'form-control'}),
            'score': forms.NumberInput(attrs={'class':'form-control'}),
        }
