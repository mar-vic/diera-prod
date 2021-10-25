from datetime import date

from django import forms


class MonthYearSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        months = [(month, month) for month in range(1, 13)]
        current_year = date.today().year
        years = [(year, year) for year in range(current_year - 1, current_year + 2)]
        widgets = [
            forms.Select(attrs={'label': 'Month'}, choices=months),
            forms.Select(attrs={'label': 'Year'}, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.month, value.year]
        elif isinstance(value, str):
            year, month = value.split('-')
            return [month, year]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-1'.format(year, month)
