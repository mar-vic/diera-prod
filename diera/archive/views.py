from urllib.parse import urlparse

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page

from cms.models import Page

from photologue.models import Gallery

from . import queries


class IndexList(ListView):
    template_name = "archive/archive.html"
    paginate_by = 2
    model = Gallery
    context_object_name = "galleries"

    def get_queryset(self):
        return Gallery.objects.filter(is_public__exact=True)


class GalleryList(ListView):
    template_name = "archive/partials/_photo-archive.html"
    paginate_by = 2
    model = Gallery
    context_object_name = "galleries"

    def get_queryset(self):
        # breakpoint()
        return Gallery.objects.filter(is_public__exact=True)


class EventList(ListView):
    template_name = "archive/partials/_programming-archive.html"
    paginate_by = 3
    model = Page
    context_object_name = "events"

    def get_queryset(self):
        # breakpoint()
        return queries.get_all_published_events()

class VideoList(ListView):
    template_name = "archive/partials/_video-archive.html"
    paginate_by = 3
    context_object_name = "videos"

    def get_queryset(self):
        # breakpoint()
        return queries.get_all_yt_videos();

class AudioList(ListView):
    template_name = "archive/partials/_audio-archive.html"
    paginate_by = 3
    context_object_name = "albums"

    def get_queryset(self):
        return queries.get_all_bandcamp_albums()

class SearchResults(TemplateView):
    template_name = "archive/partials/_search-results-masonry.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # breakpoint()

        if context["page"] == '0':
            context["result_page"] = 0
            return context
        elif context["page"] == '1':
            query = self.request.GET.get("q")
            if not query:
                context["result_page"] = 0
                context["page"] = 0
                return context
            context["query"] = query
        else:
            query = context["query"]

        context["result_page"] = Paginator(queries.query_content(query), self.paginate_by).get_page(context["page"])
        return context
