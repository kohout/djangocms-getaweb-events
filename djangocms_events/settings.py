# -*- coding: utf-8 -*-
from django.conf import settings

# easy thumbnails settings for preview displays (admin view)
IMG_OPTIONS_PREVIEW = getattr(settings, 'EVENTS_IMG_OPTIONS_PREVIEW',
                              {'size': (64, 64), 'crop': True, 'upscale': True})

# easy thumbnails settings for event image displays
IMG_OPTIONS_DETAIL = getattr(settings, 'EVENTS_IMG_OPTIONS_DETAIL',
                             {'size': (250, 250), 'crop': False, 'upscale': False})

# if djangocms_news is installed, this setting can be used to create a connection between an event and a newsitem
NEWS_CONNECTION = getattr(settings, 'EVENTS_NEWS_CONNECTION',
                          False)

# if true, filter requests will be sent via ajax and the list container will be dynamically updated.
# if false, page reload will occur
FILTER_USING_AJAX = getattr(settings, 'EVENTS_FILTER_USING_AJAX',
                            True)

