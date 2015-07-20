# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer

from djangocms_events import settings
from djangocms_events.forms import EventForm
from djangocms_events.models import Tag, Event


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_count')
    search_fields = ('name', )


class EventAdmin(admin.ModelAdmin):
    list_display = ('render_preview', 'name', '_get_description', 'get_dates_formatted')
    list_display_links = ('render_preview', 'name', )
    search_fields = ('name', 'description', 'start_date', 'start_time', 'end_date', 'end_time')
    readonly_fields = ('render_preview', )
    form = EventForm

    def _get_description(self, obj):
        return obj.description
    _get_description.allow_tags = True
    _get_description.short_description = _(u'Description')

    def render_preview(self, event):
        event_image = event.image
        if not event_image:
            return u''

        img_options = settings.IMG_OPTIONS_PREVIEW
        thumb_url = get_thumbnailer(event_image).get_thumbnail(img_options).url
        if not thumb_url:
            return u''
        return u'<img src="%s">' % thumb_url
    render_preview.allow_tags = True
    render_preview.short_description = _(u'Preview')

admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
