import datetime

from django.forms import Widget
from django.forms.widgets import Input
from django.utils import timezone


class DateTimeWidget(Input):
    input_type = 'datetime-local'

    def get_context(self, name, value, attrs):
        attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        context = super().get_context(name, value, attrs)
        return context