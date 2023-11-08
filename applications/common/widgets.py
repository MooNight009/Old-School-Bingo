import datetime

from django.forms import Widget
from django.forms.widgets import Input, NumberInput
from django.utils import timezone


class DateTimeWidget(Input):
    input_type = 'datetime-local'

    def get_context(self, name, value, attrs):
        attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        context = super().get_context(name, value, attrs)
        return context


class RangeWidget(NumberInput):
    input_type = 'range'

    def get_context(self, name, value, attrs):
        # attrs['min'] = "1"
        # attrs['max'] = '20'
        # attrs['step'] = '1'
        attrs['oninput'] = "this.nextElementSibling.value = this.value"
        context = super().get_context(name, value, attrs)
        return context