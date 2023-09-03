from django import forms

from applications.submission.models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['img', 'comment']
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control bg-alabaster border-green4'}),
            'comment': forms.TextInput(attrs={'class': 'form-control bg-alabaster border-green4'})
        }
        labels = {
            'img': 'Image:',
            'comment':'Comment:'
        }
