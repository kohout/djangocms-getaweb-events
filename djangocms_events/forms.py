# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from djangocms_events.models import Event


class EventForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start_date = cleaned_data.get('start_date', None)
        end_date = cleaned_data.get('end_date', None)
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date has to be later than start date!')
        if start_date and end_date and start_date == end_date:
            start_time = cleaned_data.get('start_time', None)
            end_time = cleaned_data.get('end_time', None)
            if start_time and end_time and end_time < start_time:
                raise ValidationError('End date has to be later than start date!')

        return super(EventForm, self).clean()

    class Meta:
        model = Event
