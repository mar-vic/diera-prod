from django.conf.urls import *

from photologue.views import GalleryArchiveIndexView, GalleryListView

urlpatterns = [
    url(r'^gallerylist/$',
        GalleryListView.as_view(),
        name='photologue-cms-integration-gallery-list'),
    url(r'',
        GalleryArchiveIndexView.as_view(),
        name='pohtologue-cms-integration-gallery-archive-index'),
]
