# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.utils.translation import ugettext as _
from tinymce.models import HTMLField


class Tag(models.Model):
    """
    Events can be tagged, which makes it easier to filter or group them.
    """
    name = models.CharField(
        max_length=255,
        help_text=_(u'Name of a tag, e.g. "Music", which allow for customized grouping or filtering.'),
        verbose_name=_(u'Name'))

    def tag_count(self):
        return self.event_set.all().count()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Tag')
        verbose_name_plural = _(u'Tags')

class Event(models.Model):
    """
    A simple event with some descriptive text.
    """
    name = models.CharField(
        max_length=255,
        help_text=_(u'Name of the event, e.g. "Music Festival".'),
        verbose_name=_(u'Event name'))

    description = HTMLField(
        blank=True, null=True,
        help_text=_(u'Description of the event containing HTML tags, e.g. '
                    u'"<p>The <b>Donauinselfest</b> (German for Danube Island Festival) '
                    u'is an open-air free music festival.</p>'),
        verbose_name=_(u'Description'))

    tags = models.ManyToManyField(
        Tag,
        blank=True, null=True,
        help_text=_(u'Tags of the event, e.g. "Music", which allow for customized grouping or filtering.'),
        verbose_name=_(u'Tags'))

    start_date = models.DateField(
        blank=True, null=True,
        help_text=_(u'The start date of the event, e.g. "26. 06. 2015".'),
        verbose_name=_(u'Start date'))

    start_time = models.TimeField(
        blank=True, null=True,
        help_text=_(u'The start time of the event, e.g. "10:00".'),
        verbose_name=_(u'Start time'))

    end_date = models.DateField(
        blank=True, null=True,
        help_text=_(u'The end date of the event, e.g. "28. 06. 2015".'),
        verbose_name=_(u'End date'))

    end_time = models.TimeField(
        blank=True, null=True,
        help_text=_(u'The end time of the event, e.g. "23:59".'),
        verbose_name=_(u'End time'))

    def display_dates(self):
        start_date = None if self.start_date is None else str(self.start_date)
        start_time = None if self.start_time is None else str(self.start_time)
        end_date = None if self.end_date is None else str(self.end_date)
        end_time = None if self.end_time is None else str(self.end_time)

        start = u' '.join(filter(None, [start_date, start_time]))
        end = u' '.join(filter(None, [end_date, end_time]))
        return u' - '.join(filter(None, [start, end]))

    def get_absolute_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Event')
        verbose_name_plural = _(u'Events')


class EventsList(CMSPlugin):
    category = models.ForeignKey(
        Tag,
        verbose_name=_(u'Category'))

    def get_items(self, category):
        items = Event.objects.filter(tags__in=category)
        return items

    class Meta:
        verbose_name = _(u'Events List Plugin')
        verbose_name_plural = _(u'Events List Plugins')
