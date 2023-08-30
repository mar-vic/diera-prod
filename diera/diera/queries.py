from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from cms.models import Page

def get_upcoming_events():
    current_year = datetime.today().year
    current_month = datetime.today().month
    current_day = datetime.today().day

    # Load all upcoming published events
    all_events = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False)[0].get_child_pages()

    def upcoming_event_p(event):
        """Tests whether given event is an upcoming one"""
        try:
            event_date_from = event.eventdataextension.date_from

            # Event is scheduled for this month in the future
            if event_date_from.year == current_year and event_date_from.month == current_month and event_date_from.day >= current_day:
                return True

            # Event is scheduled for this year in the following months (but not current one)
            if event_date_from.year == current_year and event_date_from.month > current_month:
                return True

            # Event is scheduled for following year
            if event_date_from.year > current_year:
                return True

            # Otherwise the event took place in the past
            return False
        except ObjectDoesNotExist: # Event is not scheduled yet
            return False

    # Remove all unscheduled or past events and sort remaining events according
    # to their scheduling in ascending order.
    upcoming_events = sorted(
        filter(lambda event: upcoming_event_p(event), all_events),
        key=lambda event: event.eventdataextension.date_from,
        reverse=False)

    return upcoming_events
