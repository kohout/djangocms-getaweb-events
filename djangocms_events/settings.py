# -*- coding: utf-8 -*-
from django.conf import settings

# easy thumbnails settings for preview displays (admin view)
IMG_OPTIONS_PREVIEW = getattr(settings, 'EVENTS_IMG_OPTIONS_PREVIEW',
                              {'size': (64, 64), 'crop': True, 'upscale': True})

# easy thumbnails settings for event image displays
IMG_OPTIONS_DETAIL = getattr(settings, 'EVENTS_IMG_OPTIONS_DETAIL',
                             {'size': (250, 250), 'crop': False, 'upscale': False})

