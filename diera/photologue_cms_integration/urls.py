from django.conf.urls import *
from django.urls import path, re_path

from photologue.views import GalleryArchiveIndexView, GalleryYearArchiveView

urlpatterns = [
    # re_path(r'^',
    #     GalleryArchiveIndexView.as_view(),
    #     name='pli-gallery-archive'),
    # re_path(r'^(?P<year>\d{4})/$',
    #         GalleryYearArchiveView.as_view(),
    #         name='pli-gallery-archive-year'),
    path('',
         GalleryArchiveIndexView.as_view(),
         name='pli-gallery-archive'),
    path('<year>/',
         GalleryYearArchiveView.as_view(),
         name='pli-gallery-year-archive')
]
