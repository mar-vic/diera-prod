from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.IndexList.as_view(), name='index'),
]

htmx_urlpatterns = [
    path("fotky/page<int:page>/", views.GalleryList.as_view(), name="photos"),
    path("program/page<int:page>/", views.EventList.as_view(), name="programming"),
    path("video/page<int:page>/", cache_page(60 * 60 * 24)(views.VideoList.as_view()), name="video"),
    path("audio/page<int:page>/", views.AudioList.as_view(), name="audio")
    # path("audio/page<int:page>/", cache_page(60 * 60 * 24 * 7)(views.AudioList.as_view()), name="audio")
]

urlpatterns += htmx_urlpatterns
