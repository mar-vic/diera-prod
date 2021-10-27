from django.urls import path

from . import views

app_name = 'event_calendar'

urlpatterns = [
    path('', views.event_calendar, name='calendar'),
    path('<int:year>/<int:month>/', views.event_calendar, name='calendar')
]
