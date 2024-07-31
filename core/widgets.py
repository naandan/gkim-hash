from django import forms

class DateInput(forms.DateInput):

    DATE_INPUT_WIDGET_REQUIRED_FORMAT = '%Y-%m-%d'

    def __init__(self, attrs={}, format=None):
        attrs.update({'class': 'form-control', 'type': 'date'})

        self.format = format or self.DATE_INPUT_WIDGET_REQUIRED_FORMAT
        super().__init__(attrs, format=self.format)

class TimeInput(forms.TimeInput):

    TIME_INPUT_WIDGET_REQUIRED_FORMAT = '%H:%M'

    def __init__(self, attrs={}, format=None):
        attrs.update({'class': 'form-control vTimeField w-100', 'type': 'time'})

        self.format = format or self.TIME_INPUT_WIDGET_REQUIRED_FORMAT
        super().__init__(attrs, format=self.format)

