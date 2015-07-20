# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from djangocms_events.views import EventDetailView

urlpatterns = patterns(
    '',
    url(r'^event/(?P<pk>[\w-]+)/$',
        EventDetailView.as_view(),
        name='event-detail'),
)