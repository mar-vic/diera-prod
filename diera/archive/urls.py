from django.urls import path

from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.IndexList.as_view(), name='index'),
]


htmx_urlpatterns = [
    path("fotky/page<int:page>/", views.GalleryList.as_view(), name="photos"),
    path("program/page<int:page>/", views.EventList.as_view(), name="programming"),
    path("video/", views.video, name="video"),
    path("audio/", views.audio, name="audio")
]

urlpatterns += htmx_urlpatterns
