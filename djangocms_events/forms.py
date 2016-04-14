# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from djangocms_events.models import Event


class EventForm(forms.ModelForm):
    def check_start_end(self, cleaned_data):
        start_date = cleaned_data.get('start_date', None)
        end_date = cleaned_data.get('end_date', None)
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date has to be later than start date!')
        if start_date and end_date and start_date == end_date:
            start_time = cleaned_data.get('start_time', None)
            end_time = cleaned_data.get('end_time', None)
            if start_time and end_time and end_time < start_time:
                raise ValidationError('End date has to be later than start date!')

    def check_link(self, cleaned_data):
        cms_link = cleaned_data.get('cms_link', None)
        external_link = cleaned_data.get('external_link', None)

        if cms_link and external_link:
            raise ValidationError('Please only enter a CMS page link OR an external link!')

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        self.check_start_end(cleaned_data)
        self.check_link(cleaned_data)

        return super(EventForm, self).clean()

    class Meta:
        model = Event
        exclude = ('id',)
