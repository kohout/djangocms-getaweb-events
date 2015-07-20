# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_events.models import EventsList


class EventsPlugin(CMSPluginBase):
    model = EventsList
    name = _(u'Events List')
    render_template = 'djangocms_events/list.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['items'] = instance.get_items()
        return context

plugin_pool.register_plugin(EventsPlugin)
