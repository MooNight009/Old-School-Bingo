from django import forms

from applications.common.validators import validate_string_special_free
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

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        validate_string_special_free(comment)
        return comment

