from datetime import date, timedelta, datetime

from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.inclusion_tag('archive/partials/_event-teaser.html', takes_context=True)
def event_teaser(context):
    return {
        "title": context["event"].get_page_title(),
        "url": context["event"].get_absolute_url(),
        "id": context["event"].id,
        "date": context["event"].eventdataextension.date_from,
        "image": context["event"].imageextension.image,
        "request": context["request"]
    }

