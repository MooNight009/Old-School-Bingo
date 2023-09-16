from django import forms

from applications.invocation.models import WOMInvo


class EditInvocationForm(forms.ModelForm):
    class Meta:
        exclude = ['tile']


class EditWOSInvoForm(EditInvocationForm):
    class Meta:
        model = WOMInvo
        fields = ['type', 'amount', 'names']

        widgets = {

        }