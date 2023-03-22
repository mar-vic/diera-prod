from random import randint
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import calendar as cal

from django import template
from django.core.exceptions import ObjectDoesNotExist

from filer.models.filemodels import File
from filer.models.foldermodels import Folder

from event_calendar import queries

register = template.Library()


@register.simple_tag
def month_name(month):
    return cal.month_name[month]

@register.simple_tag(takes_context=True)
def get_random_infographics_url(context, year, month):
    """
    Return the url of image to be shown instead of the calendar for months
    without (upcoming) programming.
    """
    current_year = datetime.today().year
    current_month = datetime.today().month
    # language = context['current_language']
    language = 'sk'

    if year < current_year:
        try:
            folder = Folder.objects.get(name='ig_under_construction_' + language)
        except ObjectDoesNotExist:
            return None
    elif year == current_year and month < current_month:
        try:
            folder = Folder.objects.get(name='ig_under_construction_' + language)
        except ObjectDoesNotExist:
            return None
    elif year == current_year and month == current_month:
         try:
            folder = Folder.objects.get(name='ig_see_you_' + language)
         except ObjectDoesNotExist:
            return None
    else:
        try:
            folder = Folder.objects.get(name='ig_coming_soon_' + language)
        except ObjectDoesNotExist:
            return None

    infographics_img_files = folder.files.all()
    if (len(infographics_img_files) > 0):
        rnd_infographics = infographics_img_files[
            randint(0, len(infographics_img_files) - 1)
        ]
        return rnd_infographics.url
    else:
        return None

class CalendarGrid:
    def __init__(self, year, month):
        self.eteasers_for_month = []
        self.upcoming_eteasers = []

        scheduled_events_for_month = queries.get_scheduled_events_for_month(year, month)

        for monthday in cal.Calendar().itermonthdates(year, month):
            if monthday.year == year and monthday.month == month:
                scheduled_events_for_day = scheduled_events_for_month.filter(eventdataextension__date_from__day=monthday.day)
                eteasers_for_day = []

                for event in scheduled_events_for_day:
                    eteaser = {}

                    eteaser['event_title'] = event.get_page_title()
                    eteaser['event_url'] = event.get_absolute_url()
                    eteaser['page_id'] = event.id

                    eteaser['date_from'] = event.eventdataextension.date_from
                    eteaser['date_to'] = event.eventdataextension.date_to
                    eteaser['festival'] = event.eventdataextension.festival
                    eteaser['image'] = event.imageextension.image

                    eteasers_for_day.append(eteaser)

                    # Add pairs of teasers to upcoming list
                    if eteaser['date_from'].month != date.today().month or (eteaser['date_from'].year == year and eteaser['date_from'].month == month and eteaser['date_from'].day >= date.today().day):
                        if len(self.upcoming_eteasers) > 0:
                            last_pair = next(reversed(self.upcoming_eteasers))
                            if len(last_pair) < 2:
                                last_pair.append(eteaser)
                            else:
                                self.upcoming_eteasers.append([eteaser])
                        else:
                            self.upcoming_eteasers.append([eteaser])

                self.eteasers_for_month.append((monthday.day, eteasers_for_day))
            else:
                self.eteasers_for_month.append((0, []))

    def __iter__(self):
        self.slice_index = (0,7)
        return self

    def __next__(self):
        result = self.eteasers_for_month[self.slice_index[0]:self.slice_index[1]]
        if result:
            self.slice_index = (self.slice_index[1], self.slice_index[1] + 7)
            return result
        else:
            raise StopIteration

@register.inclusion_tag('event_calendar/includes/calendar.html', takes_context=True)
def calendar(context, year, month):
    program_date = date(year=year, month=month, day=1)
    grid = CalendarGrid(year, month)

    return {
        "eteasers_for_month": grid,
        'program_date': program_date,
        'request': context.request,
        # 'current_language': context['current_language'],
        'current_language': 'sk',
        'calNavForm': context['calNavForm']
    }


@register.inclusion_tag('event_calendar/includes/upcoming_events.html', takes_context=True)
def upcoming_event_teasers(context, date_from=date.today(), date_to=(date.today() + timedelta(days=14))):
    events = queries.get_all_published_events()
    eteasers = []

    for event in events:
        eteaser = {}

        # ignore unscheduled events
        try:
            eteaser['date_from'] = event.eventdataextension.date_from

            if not (eteaser['date_from'].date() >= date_from and eteaser['date_from'].date() <= date_to):
                continue

            eteaser['date_to'] = event.eventdataextension.date_to
            eteaser['festival'] = event.eventdataextension.festival
        except ObjectDoesNotExist:
            continue

        # use default values for events with uninitialized teaser extension
        try:
            eteaser['image'] = event.imageextension.image
        except ObjectDoesNotExist:
            eteaser['image'] = None

        eteaser['event_title'] = event.get_page_title()
        eteaser['event_url'] = event.get_absolute_url()
        eteaser['page_id'] = event.id

        eteasers.append(eteaser)

    return {
        'eteasers': eteasers,
        'request': context.request,
    }

@register.simple_tag
def get_hr_time_span(date):
    """
    Return human readable time span.
    """
    # breakpoint()
    today = datetime.today()
    today = datetime(today.year, today.month, today.day)
    date = datetime(date.year, date.month, date.day)
    delta = date - today

    if delta.days == 0: return 'dnes'
    if delta.days == 1: return 'zajtra'
    if delta.days >= 2 and delta.days <= 7: return date.strftime("%A")
    if delta.days > 7 and delta.days <= 14: return 'o týždeň'
    if delta.days > 14 and delta.days <= 30: return 'o 2 týždne'
    if delta.days > 30 and delta.days <= 60: return 'o mesiac'

    return None

@register.simple_tag
def get_background_image_url_for_month(year, month):
    """
    Return the url of an image to be used as site background from the
    'background_images' folder. The image is chosen according to following rules:
    1) return image named 'current'; 2) otherwise return image named '<current
    year>_<current_month>; 3) otherwise return the url of last uploaded image;
    4) finally, if there is no image in the folder, return empty string, thus
    making the site with haveing no background image.
    """
    today = date.today()
    try:
        folder = Folder.objects.get(name='background_images')
    except ObjectDoesNotExist:
        return ''

    bgimage_by_flag = folder.files.filter(name='current').first()
    bgimage_by_date = folder.files.filter(name=f"{year}_{month}").first()
    bgimage_by_uploaded = folder.files.order_by('-uploaded_at').first()

    if bgimage_by_flag:
        return bgimage_by_flag.url
    elif bgimage_by_date:
        return bgimage_by_date.url
    elif bgimage_by_uploaded:
        return bgimage_by_uploaded.url
    else:
        return ''
