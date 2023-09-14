import datetime

from django.forms import Widget
from django.forms.widgets import Input


class DateTimeWidget(Input):
    input_type = 'datetime-local'

    def get_context(self, name, value, attrs):
        attrs['min'] = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M')
        # attrs['value'] = '2018-06-12T19:30'
        # attrs['max'] = '2018-06-12T19:30'
        context = super().get_context(name, value, attrs)
        return context