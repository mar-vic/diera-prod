from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views.decorators.cache import cache_page

from cms.models import Page

from photologue.models import Gallery

from . import queries


class IndexList(ListView):
    template_name = "archive/archive.html"
    paginate_by = 3
    model = Gallery
    context_object_name = "galleries"


class GalleryList(ListView):
    template_name = "archive/partials/_photo-archive.html"
    paginate_by = 3
    model = Gallery
    context_object_name = "galleries"


class EventList(ListView):
    template_name = "archive/partials/_programming-archive.html"
    paginate_by = 3
    model = Page
    context_object_name = "events"

    def get_queryset(self):
        return queries.get_all_published_events()

class VideoList(ListView):
    template_name = "archive/partials/_video-archive.html"
    paginate_by = 3
    context_object_name = "videos"

    def get_queryset(self):
        return queries.get_all_yt_videos();

class AudioList(ListView):
    template_name = "archive/partials/_audio-archive.html"
    paginate_by = 3
    context_object_name = "albums"

    def get_queryset(self):
        return queries.scrape_all_bandcamp_albums()

def index(request):
    return render(request, 'archive/archive.html')

def photos(request):
    return render(request, "archive/partials/_photo-archive.html")

def programming(request):
    print(request.GET['page'])
    return render(request, template_name="archive/partials/_programming-archive.html", context={"page":request.GET["page"]})

def video(request):
    return render(request, "archive/partials/_video-archive.html")

def audio(request):
    return render(request, "archive/partials/_audio-archive.html")


