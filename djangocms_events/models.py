# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from cms.models.pagemodel import Site, Page
from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.db.models.query_utils import Q
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from easy_thumbnails.fields import ThumbnailerImageField
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

    target_page = models.ForeignKey(
        Site,
        blank=True, null=True,
        help_text=_(u'Event is associated with a certain page.'),
        verbose_name=_(u'Target Page'))

    image = ThumbnailerImageField(
        upload_to='djangocms_events/',
        blank=True, null=True,
        help_text=_(u'Image of Event.'),
        verbose_name=_(u'Image'))

    description = HTMLField(
        blank=True, null=True,
        help_text=_(u'Description of the event containing HTML tags, e.g. '
                    u'"The <b>Donauinselfest</b> (German for <i>Danube Island Festival</i>) '
                    u'is an open-air free music festival.".'),
        verbose_name=_(u'Description'))

    cms_link = models.ForeignKey(
        Page,
        blank=True, null=True,
        help_text=_(u'A link to a page on this website, e.g. "/donauinselfest/".'),
        verbose_name=_(u'CMS page link'))

    external_link = models.URLField(
        blank=True, null=True,
        help_text=_(u'A link that provides further information about the event, e.g. '
                    u'"https://2015.donauinselfest.at/".'),
        verbose_name=_(u'External link'))

    link_title = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'Title that is displayed and wrapped with either CMS page link or External link, e.g. '
                    u'"More information".'),
        verbose_name=_(u'Link title'))

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

    @property
    def get_dates_formatted(self):
        start = self.get_start_formatted
        end = self.get_end_formatted
        return mark_safe(u' <br /> '.join(filter(None, [start, end])))

    @property
    def get_start_formatted(self):
        start_date = self.start_date.strftime('%d. %m. %Y') if self.start_date else None
        start_time = str(self.start_time) if self.start_time else None
        start = u', '.join(filter(None, [start_date, start_time]))
        if start:
            return _(u'Start: ') + start
        else:
            return ''

    @property
    def get_end_formatted(self):
        end_date = self.end_date.strftime('%d. %m. %Y') if self.end_date else None
        end_time = str(self.end_time) if self.end_time else None
        end = u', '.join(filter(None, [end_date, end_time]))
        if end:
            return _(u'End: ') + end
        else:
            return ''

    def get_set_link(self):
        if self.cms_link:
            return self.cms_link.get_absolute_url()
        elif self.external_link:
            return self.external_link
        else:
            return None

    def get_link_title(self):
        return self.link_title if self.link_title else self.get_set_link()

    @property
    def get_link_str(self):
        link = self.get_set_link()
        if not link:
            return ''

        res = u''.join(['<a href="', link, '" target="_blank">', self.get_link_title(), '</a>'])
        return mark_safe(res)

    def get_absolute_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u'Event')
        verbose_name_plural = _(u'Events')
        ordering = ['start_date', 'start_time', 'end_date', 'end_time']


ARCHIVE_CHOICES = (
    ('all', _(u'All Events')),
    ('past', _(u'Past Events')),
    ('future', _(u'Future Events')),
)


class EventsList(CMSPlugin):
    title = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_(u'The title that is displayed above the events list.'),
        verbose_name=_(u'Title'))

    category = models.ManyToManyField(
        Tag,
        blank=True, null=True,
        help_text=_(u'Only show events with these tags.'),
        verbose_name=_(u'Category'))

    archive = models.CharField(
        choices=ARCHIVE_CHOICES,
        default=ARCHIVE_CHOICES[0],
        max_length=50,
        help_text=_(u'Filter by event dates.'),
        verbose_name=_(u'Archive mode'))

    max_item_count = models.PositiveIntegerField(
        default=0,
        help_text=_(u'Maximum number of items to display. Enter "0" for no boundaries.'),
        verbose_name=_(u'Max. item count'))

    target_page = models.ForeignKey(
        Site,
        blank=True, null=True,
        help_text=_(u'Only display events associated with this page.'),
        verbose_name=_(u'Target Page'))

    def get_items(self):
        items = Event.objects.all()
        f = Q()

        if self.target_page:
            f = (Q(target_page=self.target_page))

        if self.archive == 'past':
            # either no dates entered
            # or end date entered and end date is in the past
            # or start date entered (but no end date) and start date is in the past
            f = f & (
                (Q(start_date__isnull=True) & Q(end_date__isnull=True)) |
                (Q(end_date__isnull=False) & Q(end_date__lt=now())) |
                (Q(end_date__isnull=True) & Q(start_date__isnull=False) & Q(start_date__lt=now()))
            )
        elif self.archive == 'future':
            # either no dates entered
            # or or end date entered and end date is in the future
            # or start date entered (but no end date) and start date is in the future
            f = f & (
                (Q(start_date__isnull=True) & Q(end_date__isnull=True)) |
                (Q(end_date__isnull=False) & Q(end_date__gt=now())) |
                (Q(end_date__isnull=True) & Q(start_date__isnull=False) & Q(start_date__gt=now()))
            )

        if self.category.all():
            f = f & Q(tags__in=self.category.all())

        if self.max_item_count > 0:
            return items.filter(f)[:self.max_item_count]

        return items.filter(f)

    def __unicode__(self):
        res = self.title if self.title else _(u'Event list')
        if self.category.all():
            cats = u', '.join([t.name for t in self.category.all()])
            res = u''.join(filter(None, [res, u' (', cats, u')']))
        return res

    class Meta:
        verbose_name = _(u'Events List Plugin')
        verbose_name_plural = _(u'Events List Plugins')
