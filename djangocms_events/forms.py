# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from djangocms_events.models import Event


class EventForm(forms.ModelForm):
    description = forms.CharField(widget=TinyMCE(attrs={'plugins': 'image'}))

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        start_date = cleaned_data.get('start_date', None)
        end_date = cleaned_data.get('end_date', None)
        if end_date < start_date:
            raise ValidationError('End date has to be later than start date!')

        return super(EventForm, self).clean()

    class Meta:
        model = Event
