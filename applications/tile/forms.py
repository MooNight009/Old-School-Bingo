from django import forms

from applications.invocation.models import Invocation
from applications.tile.models import Tile


class TileForm(forms.ModelForm):
    class Meta:
        model = Tile
        fields = ['name', 'description']


class EditTileForm(forms.ModelForm):
    class Meta:
        model = Tile
        fields = ['name', 'description', 'img', 'score', 'invocation_type']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control w-25'}),
            'description': forms.Textarea(attrs={'class':'form-control w-50'}),
            'img': forms.FileInput(attrs={'class':'form-control w-25'}),
            'score': forms.NumberInput(attrs={'class':'form-control w-25'}),
            'invocation_type': forms.Select(attrs={'class':'btn-default rounded-3'})
        }