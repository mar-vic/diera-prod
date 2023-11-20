from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.IndexList.as_view(), name='index'),
]

htmx_urlpatterns = [
    path("fotky/page<int:page>/", views.GalleryList.as_view(), name="photos"),
    path("fotky/<int:year>/page<int:page>/", views.GalleryList.as_view(), name="photos"),
    path("fotky/<int:year>/<int:month>/page<int:page>/", views.GalleryList.as_view(), name="photos"),
    path("program/page<int:page>/", views.EventList.as_view(), name="programming"),
    path("video/page<int:page>/", views.VideoList.as_view(), name="video"),
    path("audio/page<int:page>/", views.AudioList.as_view(), name="audio"),
    path("search-results/", views.SearchResults.as_view(), name="search-results"),
    path("search-results/page<int:page>/", views.SearchResults.as_view(), name="search-results"),
    path("search-results/page<int:page>/query<query>/", views.SearchResults.as_view(), name="search-results")
]

urlpatterns += htmx_urlpatterns
