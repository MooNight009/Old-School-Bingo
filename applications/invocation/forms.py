from django import forms

from applications.invocation.models import WOMInvo, BOSSES, SKILLS


class EditInvocationForm(forms.ModelForm):
    class Meta:
        exclude = ['tile']


class EditWOSInvoForm(EditInvocationForm):
    class Meta:
        model = WOMInvo
        fields = ['type', 'amount', 'names']

        widgets = {
            'type' : forms.Select(attrs={'class':'btn-default rounded-3'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control w-25', 'min':'1'}),
            'names': forms.TextInput(attrs={'class':'form-control w-25'}),
        }

        labels = [

        ]

    def clean(self):
        cleaned_data = self.cleaned_data
        names = cleaned_data['names'].lower().split(',')

        if self.cleaned_data['type'] == 'KC':
            for name in names:
                if name not in BOSSES:
                    raise forms.ValidationError({'names': [f'{name} is not a boss name. Available names are {BOSSES}']})
        else:
            for name in names:
                if name not in SKILLS:
                    raise forms.ValidationError({'names': [f'{name} is not a skill name. Available names are {SKILLS}']})

        return cleaned_data
