# -*- coding: utf-8 -*-
from django.views.generic.detail import DetailView
from djangocms_events.models import Event


class EventDetailView(DetailView):
    model = Event
    template_name = 'djangocms_events/detail.html'
