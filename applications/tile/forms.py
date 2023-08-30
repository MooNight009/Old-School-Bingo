from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from applications.submission.models import Submission
from applications.tile.models import Tile


class TileForm(forms.ModelForm):
    class Meta:
        model = Tile
        fields = ['name', 'description']


# class SubmissionForm(forms.ModelForm)
#     class Meta:
#         model = Submission
#         fields = ['img', 'comment']
#
#
#     def __int__(self, *args, **kwargs):
#         super().__int__(*args, **kwargs)
#         self.fields['comment'].widget = forms.TextInput(attrs={'class':'form-control'})
#         self.fields['img'].widget = forms.FileInput(attrs={'class':'form-control'})
