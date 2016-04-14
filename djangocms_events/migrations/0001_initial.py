# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('sites', '0001_initial'),
        ('djangocms_news', '0004_auto_20160414_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the event, e.g. "Music Festival".', max_length=255, verbose_name='Event name')),
                ('highlight', models.BooleanField(default=False, help_text='Whether event should be highlighted in teaser list.', verbose_name='Is highlight')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(help_text='Image of Event.', upload_to=b'djangocms_events/', null=True, verbose_name='Bild', blank=True)),
                ('description', tinymce.models.HTMLField(help_text='Description of the event containing HTML tags, e.g. "The <b>Donauinselfest</b> (German for <i>Danube Island Festival</i>) is an open-air free music festival.".', null=True, verbose_name='Beschreibung', blank=True)),
                ('external_link', models.URLField(help_text='A link that provides further information about the event, e.g. "https://2015.donauinselfest.at/".', null=True, verbose_name='External link', blank=True)),
                ('link_title', models.CharField(help_text='Title that is displayed and wrapped with either CMS page link or External link, e.g. "More information".', max_length=255, null=True, verbose_name='Link title', blank=True)),
                ('start_date', models.DateField(help_text='The start date of the event, e.g. "26. 06. 2015".', null=True, verbose_name='Start date', blank=True)),
                ('start_time', models.TimeField(help_text='The start time of the event, e.g. "10:00".', null=True, verbose_name='Start time', blank=True)),
                ('end_date', models.DateField(help_text='The end date of the event, e.g. "28. 06. 2015".', null=True, verbose_name='End date', blank=True)),
                ('end_time', models.TimeField(help_text='The end time of the event, e.g. "23:59".', null=True, verbose_name='End time', blank=True)),
                ('associated_news', models.ForeignKey(blank=True, to='djangocms_news.NewsItem', help_text='The associated news item.', null=True, verbose_name='News item')),
                ('cms_link', models.ForeignKey(blank=True, to='cms.Page', help_text='A link to a page on this website, e.g. "/donauinselfest/".', null=True, verbose_name='CMS page link')),
                ('sites', models.ManyToManyField(help_text='Event is associated with a certain site.', to='sites.Site', null=True, verbose_name='Site', blank=True)),
            ],
            options={
                'ordering': ['start_date', 'start_time', 'end_date', 'end_time'],
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventsList',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(help_text='The title that is displayed above the events list.', max_length=255, null=True, verbose_name='Titel', blank=True)),
                ('render_mode', models.CharField(default=b'list.html', help_text='How the list of events should be displayed.', max_length=255, verbose_name='Display mode', choices=[(b'list.html', 'List'), (b'teaser.html', 'Teaser')])),
                ('archive', models.CharField(default=(b'all', 'All Events'), help_text='Filter by event dates.', max_length=50, verbose_name='Archive mode', choices=[(b'all', 'All Events'), (b'past', 'Past Events'), (b'future', 'Future Events')])),
                ('max_item_count', models.PositiveIntegerField(default=0, help_text='Maximum number of items to display. Enter "0" for no boundaries.', verbose_name='Max. item count')),
            ],
            options={
                'verbose_name': 'Events List Plugin',
                'verbose_name_plural': 'Events List Plugins',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='EventTagList',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(help_text='The title that is displayed above the tag list.', max_length=255, null=True, verbose_name='Titel', blank=True)),
            ],
            options={
                'verbose_name': 'Tag List Plugin',
                'verbose_name_plural': 'Tag List Plugins',
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of a tag, e.g. "Music", which allow for customized grouping or filtering.', max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.AddField(
            model_name='eventslist',
            name='category',
            field=models.ManyToManyField(help_text='Only show events with these tags.', to='djangocms_events.Tag', null=True, verbose_name='Kategorie', blank=True),
        ),
        migrations.AddField(
            model_name='eventslist',
            name='event_list',
            field=models.ForeignKey(blank=True, to='cms.Page', help_text='Page containing a Event List Plugin with Display mode "List"', null=True, verbose_name='Event list page'),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(help_text='Tags of the event, e.g. "Music", which allow for customized grouping or filtering.', to='djangocms_events.Tag', null=True, verbose_name='Tags', blank=True),
        ),
    ]
