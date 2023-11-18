from django import forms

from applications.common.validators import validate_string_special_free
from applications.tile.models import Tile, TileImage


class EditTileForm(forms.ModelForm):
    pack_image_name = forms.ChoiceField(
        choices=tuple((x, x) for x in (list(TileImage.objects.all().values_list('name', flat=True)) + [''])),
        widget=forms.Select(attrs={'class': 'btn-default rounded-3 w-md-25'}),
        help_text='Select one of the available tile images instead of uploading. All images are taken from the wiki '
                  'and you can view them at (TO BE IMPLEMENTED)',
        required=False,
    )

    class Meta:
        model = Tile
        fields = ['name', 'description', 'pack_image_name', 'img', 'drop_count', 'score', 'invocation_type']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-md-25'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-md-50'}),
            'img': forms.FileInput(attrs={'class': 'form-control w-md-25'}),
            'drop_count': forms.NumberInput(attrs={'class': 'form-control w-md-25'}),
            'score': forms.NumberInput(attrs={'class': 'form-control w-md-25'}),
            'invocation_type': forms.Select(attrs={'class': 'btn-default rounded-3 w-md-25'})
        }

    def __init__(self, *args, **kwargs):
        super(EditTileForm, self).__init__(*args, **kwargs)
        if self.instance.bingo.is_over:
            self.fields['name'].disabled = True
            self.fields['description'].disabled = True
            self.fields['img'].disabled = True
            self.fields['score'].disabled = True
            self.fields['invocation_type'].disabled = True
            self.fields['pack_image_name'].disabled = True

    def clean_name(self):
        name = self.cleaned_data['name']
        validate_string_special_free(name)
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        validate_string_special_free(description)
        return description

    # def clean(self):
    #     cleaned_data = super(EditTileForm, self).clean()
    #
    #     return cleaned_data
