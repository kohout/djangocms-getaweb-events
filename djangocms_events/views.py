# -*- coding: utf-8 -*-
from django.db.models.query_utils import Q
from django.views.generic.detail import DetailView
from djangocms_events.models import Event

try:
    # >= Django 1.7
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site


class EventDetailView(DetailView):
    model = Event
    template_name = 'djangocms_events/detail.html'

    def get_queryset(self):
        current_site = get_current_site(self.request)
        q = Event.objects.filter(Q(sites__isnull=True) | Q(sites__id__contains=current_site.id))

        return q

    def get_next(self):
        q = self.get_queryset().filter(
            start_date__lt=self.object.start_date).order_by('-start_date', '-start_time')
        if q.count() > 0:
            return q[0]
        return None

    def get_previous(self):
        q = self.get_queryset().filter(
            start_date__gt=self.object.start_date).order_by('start_date', 'start_time')
        if q.count() > 0:
            return q[0]
        return None

    def get_context_data(self, *args, **kwargs):
        ctx = super(EventDetailView, self).get_context_data(*args, **kwargs)
        ctx['next'] = self.get_next()
        ctx['previous'] = self.get_previous()
        return ctx
