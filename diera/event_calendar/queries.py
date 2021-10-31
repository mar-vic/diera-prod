from datetime import date

from django.core.exceptions import ObjectDoesNotExist

from cms.models import Page

def get_scheduled_events_for_month(year, month):
    program_page = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False).first()
    return program_page.get_child_pages().filter(publisher_is_draft=False).filter(eventdataextension__date_from__year=year).filter(eventdataextension__date_from__month=month)

def get_scheduled_events_for_day(year, month, day):
    program_page = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False).first()
    return program_page.get_child_pages().filter(publisher_is_draft=False).filter(eventdataextension__date_from__year=year).filter(eventdataextension__date_from__month=month).filter(eventdataextension__date_from__day=day)

def get_all_published_events():
    # Load all published events
    events = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False)[0].get_child_pages()
    eventlst = []

    # Remove all events with uninitialized scheduling
    for event in events:
        try:
            extension = event.eventdataextension
            eventlst.append(event)
        except ObjectDoesNotExist:
            continue

    # Sort the list of events according to their starting date
    eventlst = sorted(eventlst,
                      key=lambda event: event.eventdataextension.date_from,
                      reverse=True)

    return list(reversed(eventlst))

def get_published_events_for_month(year, month):
    return [event for event in get_all_published_events() if
            event.eventdataextension.date_from.year == year and
            event.eventdataextension.date_from.month == month]

def get_published_events_for_day(year, month, day):
    events = []
    for event in get_published_events_for_month(year, month):
        if event.eventdataextension.date_from.day == day:
            events.append(event)
        elif event.eventdataextension.date_to and event.eventdataextension.date_from.day <= day <= event.eventdataextension.date_to.day:
            events.append(event)
    return events

def get_years_with_published_events_as_choices():
    yearsSet = set()
    yearsChoices = []

    for event in get_all_published_events():
        eventYear = event.eventdataextension.date_from.year
        if eventYear not in yearsSet:
            yearsChoices.append((eventYear, str(eventYear)))
            yearsSet.add(eventYear)
        else:
            continue

    # Append also current year, if it is already not present in choices
    currentYear = date.today().year
    if currentYear not in yearsSet:
        yearsChoices.append((currentYear, str(currentYear)))

    return reversed(yearsChoices)



