from django import forms

from applications.common.validators import validate_string_special_free
from applications.invocation.models import Invocation
from applications.tile.models import Tile


class TileForm(forms.ModelForm):
    class Meta:
        model = Tile
        fields = ['name', 'description']

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_string_special_free(name)
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        validate_string_special_free(description)
        return description


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

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_string_special_free(name)
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        validate_string_special_free(description)
        return description