from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import queries

class CalendarNavigationForm(forms.Form):
    class Months(models.TextChoices):
        JANUARY = 1, _('January')
        FEBRUARY = 2, _('February')
        MARCH = 3, _('March')
        APRIL = 4, _('April')
        MAY = 5, _('May')
        JUNE = 6, _('June')
        JULY = 7, _('July')
        AUGUST = 8, _('August')
        SEPTEMBER = 9, _('September')
        OCTOBER = 10, _('October')
        NOVEMBER = 11, _('November')
        DECEMBER = 12, _('December')

    month = forms.ChoiceField(label='Month', choices=Months.choices)
    year = forms.ChoiceField(label='Year', choices=queries.get_years_with_published_events_as_choices())

