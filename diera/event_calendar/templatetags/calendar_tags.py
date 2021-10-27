from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar as cal

from django import template
from django.core.exceptions import ObjectDoesNotExist

from filer.models.foldermodels import Folder

from event_calendar import queries

register = template.Library()


@register.simple_tag
def month_name(month):
    return cal.month_name[month]

class CalendarGrid:
    def __init__(self, year, month):
        self.eteasers_for_month = []
        self.upcoming_eteasers = []

        for monthday in cal.Calendar().itermonthdates(year, month):
            if monthday.year == year and monthday.month == month:
                events = queries.get_published_events_for_day(year, month, monthday.day)
                eteasers_for_day = []

                for event in events:
                    eteaser = {}

                    eteaser['event_title'] = event.get_page_title()
                    eteaser['event_url'] = event.get_absolute_url()
                    eteaser['page_id'] = event.id

                    eteaser['date_from'] = event.eventdataextension.date_from
                    eteaser['date_to'] = event.eventdataextension.date_to
                    eteaser['festival'] = event.eventdataextension.festival
                    eteaser['image'] = event.imageextension.image

                    eteasers_for_day.append(eteaser)

                    if eteaser['date_from'].day > date.today().day:
                        self.upcoming_eteasers.append(eteaser)

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
    }


@register.inclusion_tag('event_calendar/includes/upcoming_events.html')
def upcoming_event_teasers(date_from=date.today(), date_to=(date.today() + timedelta(days=14))):
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
            eteaser['image_url'] = event.teaserimageextension.teaser_image.url
            eteaser['text'] = event.get_title_obj().teasertextextension.teaser_text
        except ObjectDoesNotExist:
            eteaser['image_url'] = "/media/teaser_images/default_teaser_image.jpeg"
            eteaser['text'] = "write your teaser text through the 'Event Settings -> Teaser Text...' menu in toolbar"

        eteaser['event_title'] = event.get_page_title()
        eteaser['event_url'] = event.get_absolute_url()

        eteasers.append(eteaser)

    return {'eteasers': eteasers}

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
    folder = Folder.objects.get(name='background_images')

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
