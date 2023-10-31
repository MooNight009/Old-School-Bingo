from django import forms

from applications.submission.models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['img', 'comment']
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control bg-secondary-1 border-0'}),
            'comment': forms.TextInput(attrs={'class': 'form-control bg-secondary-1 border-0'})
        }
        labels = {
            'img': 'Image:',
            'comment':'Comment:'
        }

