# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_events.models import EventsList, EventTagList

try:
    # >= Django 1.7
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site


class EventsPlugin(CMSPluginBase):
    model = EventsList
    name = _(u'Events List')
    cache = False

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_events/' + instance.render_mode

    def render(self, context, instance, placeholder):
        current_site = get_current_site(context['request'])
        archive_mode = context['request'].GET.get('archive_mode', 'future')
        tags = context['request'].GET.get('tags', None)
        search = context['request'].GET.get('search', None)

        context['instance'] = instance
        context['items'] = instance.get_items(archive_mode, current_site, tags, search)
        return context


class EventFilterPlugin(CMSPluginBase):
    model = EventTagList
    name = _(u'Event Filter')
    render_template = 'djangocms_events/filter.html'

    def render(self, context, instance, placeholder):
        context['filter_instance'] = instance
        context['filter_tags'] = instance.get_items()
        return context

plugin_pool.register_plugin(EventsPlugin)
plugin_pool.register_plugin(EventFilterPlugin)
