import json
import requests
import environ
import os
import itertools
from unidecode import unidecode

from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup

from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.db.models import Q

from photologue.models import Gallery
from cms.models import Page

def get_all_published_events():
    # Load all published events
    events = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False)[0].get_child_pages()
    eventlst = []

    # Remove all events with uninitialized scheduling
    for event in events:
        try:
            extension = event.eventdataextension
            eventlst.append(event)
        except ObjectDoesNotExist:
            continue

    # Sort the list of events according to their starting date
    eventlst = sorted(eventlst,
                      key=lambda event: event.eventdataextension.date_from,
                      reverse=True)

    return list(eventlst)

def query_published_events(query, date=None):
    def query_filter(page):
        # get normalized page title (ie., without accents and in lowercase)
        title = unidecode(page.get_page_title()).lower()

        #  Exclude events with uninitialized extensions
        try:
            extension = page.eventdataextension
            extension = page.imageextension
        except ObjectDoesNotExist:
            return False

        # returns the result fo comparison
        return query in title

    events = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False)[0].get_child_pages()

    events =[(1, {"title": page.get_page_title(),
                  "image": page.imageextension.image,
                  "url": page.get_absolute_url(),
                  "id": page.id,
                  "date": page.eventdataextension.date_from})
              for page in list(filter(query_filter, events))]

    return events

def query_galleries(query, date=None):
    galleries = [(0, {"title": gallery.title,
                      "date": gallery.date_added,
                      "photos": gallery.public()
                      })
                 for gallery in Gallery.objects.filter(is_public__exact=True).filter(title__icontains=query)]

    return galleries

def get_all_yt_videos():
    videos = cache.get("yt_videos")
    if not videos:
        cache.set("yt_videos", get_all_yt_videos_api(), 60 * 60 * 24)
        return cache.get("yt_videos")
    return videos

def get_all_yt_videos_api():
    # get google api key from the .env file
    BASE_DIR = Path(__file__).resolve().parent.parent
    env = environ.Env()
    env.escape_proxy = True
    # Read environment variables from .env file
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    API_KEY = env.str("GOOGLE_API_KEY")

    teasers = []

    # Get the list of YT videos with API Request
    response  = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UC326HkT9w-FxK3ySvKfKxKQ&maxResults=100&order=date&key={API_KEY}")

    # Generate the data for teasers
    for video in response.json()["items"]:
        if video["id"]["kind"] == "youtube#video":
            teaser = {}
            teaser["title"] = video["snippet"]["title"]
            teaser["description"] = video["snippet"]["description"]
            teaser["id"] = video["id"]["videoId"]
            teasers.append(teaser)

    # print("Video query has been run!")
    return teasers

def query_yt_videos(query, date=None):
    def query_filter(video):
        # Get normalized tiel and description
        title = unidecode(video["title"]).lower()
        description = unidecode(video["description"]).lower()
        return query in title or query in description
    return [(2, video) for video in list(filter(query_filter, get_all_yt_videos()))]

def get_all_bandcamp_albums():
    albums = cache.get("bandcamp_albums")
    if not albums:
        cache.set("bandcamp_albums", scrape_all_bandcamp_albums(), 60 * 60 * 24 * 7)
        return cache.get("bandcamp_albums")
    return albums

def scrape_all_bandcamp_albums():
    # Create the soup object from bandcamp audio page
    soup = BeautifulSoup(requests.get("https://dieradosveta.bandcamp.com/audio").content, "html.parser")

    album_data = []
    # Find the tags representing the albums (ie, lis with music-grid-item class)
    album_tags = soup.find_all("li", class_="music-grid-item")

    # Extract the relevant information from the tags
    for album_tag in album_tags:
        # Extract albums id and url and construct the values needed for embedding bandcamp player
        album_id = album_tag.attrs["data-item-id"].split("-")[1] # album id extraction

        src_value = f"https://bandcamp.com/EmbeddedPlayer/album={ album_id }/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/artwork=small/transparent=true/" # construct the src value
        href_value = f"https://dieradosveta.bandcamp.com{album_tag.find('a').attrs['href']}" # construct the href value

        # Create the soup object from bandcamp album page (to extract title, description and release date)
        album_soup = BeautifulSoup(requests.get(href_value).content, "html.parser")
        # Scrape the json metadata
        metadata = json.loads(album_soup.findAll("script", type="application/ld+json")[0].contents[0])

        album_data.append({
            "src": src_value,
            "url": href_value,
            "title": metadata["name"],
            "releaseDate": metadata["dateModified"],
            "description": metadata["description"]
        })

    # print("Scraping the albums.")
    return album_data

def query_bandcamp_albums(query, date=None):
    def query_filter(album):
        title = unidecode(album["title"]).lower()
        description = unidecode(album["description"]).lower()
        return query in title or query in description
    return [(3, album) for album in list(filter(query_filter, get_all_bandcamp_albums()))]

def get_all_content():
    print("loading galleries ...")
    galleries = [(0, {"title": gallery.title,
                      "date": gallery.date_added,
                      "photos": gallery.public()
                      })
                 for gallery in Gallery.objects.filter(is_public__exact=True)]
    print("loading events ...")
    events = [(1, {"title": event.get_page_title(),
                   "date": event.eventdataextension.date_from,
                   "url": event.get_absolute_url(),
                   "id": event.id,
                   "image": event.imageextension.image
                   })
              for event in get_all_published_events()]
    print("loading videos ...")
    videos = [(2, video) for video in get_all_yt_videos()]
    print("loading audio ...")
    audio = [(3, audio) for audio in get_all_bandcamp_albums()]

    # breakpoint()

    # return {
    #     "galleries": galleries,
    #     "events": events,
    #     "videos": videos,
    #     "audio": audio
    # }

    return list(itertools.chain(galleries, events, videos, audio))

def query_content(query):
    print("querying galleries ...")
    galleries = query_galleries(query)

    print("querying events ...")
    events = query_published_events(query)

    print("Qerying YT videos ...")
    videos = query_yt_videos(query)

    print("Querying BandCamp albums")
    albums = query_bandcamp_albums(query)

    # breakpoint()

    return list(itertools.chain(galleries, events, videos, albums))




