from datetime import date

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CalendarNavigationForm


def event_calendar(request, year=date.today().year, month=date.today().month):
    """Show calendar"""

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a from instance and populate it with data from the request
        calNavForm = CalendarNavigationForm(request.POST)
        # check wether the form is valid:
        if calNavForm.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            year = calNavForm.cleaned_data['year']
            month = calNavForm.cleaned_data['month']

            # render the calendar for submitted year and month
            return render(request, 'event_calendar/calendar.html', {'year': int(year), 'month': int(month), 'calNavForm': calNavForm})

    # if a GET (or any other method) we'll create a blank form
    else:
        # Initialize form with current year and month
        calNavForm = CalendarNavigationForm(initial={'month':month, 'year': year})

    return render(request, 'event_calendar/calendar.html', {'year': int(year), 'month': int(month), 'calNavForm': calNavForm})
