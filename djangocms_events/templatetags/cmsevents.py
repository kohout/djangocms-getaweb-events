# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from easy_thumbnails.files import get_thumbnailer
from djangocms_events import settings

register = template.Library()


@register.filter()
def render_image(item):
    image = item.image
    if not image:
        return u''

    thumb_url = get_thumbnailer(image).get_thumbnail(settings.IMG_OPTIONS_DETAIL).url
    return mark_safe('<img src="%s" alt="%s" />' % (thumb_url, item.name))
