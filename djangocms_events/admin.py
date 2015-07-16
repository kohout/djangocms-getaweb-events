# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _
from djangocms_events.forms import EventForm
from djangocms_events.models import Tag, Event


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_count')
    search_fields = ('name', )

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', '_get_description', 'display_dates')
    list_display_links = ('name', )
    search_fields = ('name', 'description', 'start_date', 'start_time', 'end_date', 'end_time')
    form = EventForm

    def _get_description(self, obj):
        return obj.description
    _get_description.allow_tags = True
    _get_description.short_description = _(u'Description')

admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
