from django import forms

from applications.submission.models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['img', 'comment']
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control'}),
            'comment': forms.TextInput(attrs={'class': 'form-control'})
        }
        labels = {
            'img': 'Image:',
            'comment':'Comment:'
        }
    #
    # def __int__(self, *args, **kwargs):
    #     print("Are we here?")
    #     super().__int__(*args, **kwargs)
    #     print("We initializing submission form")
    #     print(self.fields)
    #     self.fields['comment'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['img'].widget.attrs.update({'class': 'form-control'})
