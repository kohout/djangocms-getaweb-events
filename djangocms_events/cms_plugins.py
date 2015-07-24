# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_events.models import EventsList

try:
    # >= Django 1.7
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site


class EventsPlugin(CMSPluginBase):
    model = EventsList
    name = _(u'Events List')
    render_template = 'djangocms_events/teaser.html'

    def render(self, context, instance, placeholder):
        current_site = get_current_site(context['request'])

        context['instance'] = instance
        context['items'] = instance.get_items(current_site)
        return context

plugin_pool.register_plugin(EventsPlugin)
