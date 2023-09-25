import json
import requests
import environ
import os

from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup

from django.core.exceptions import ObjectDoesNotExist

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

def get_all_yt_videos():
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

    print("Video query has been run!")
    return teasers

def get_all_bandcamp_albums():
    with open("static/diera_bandcamp_albums.json", "r") as albums_json:
        return json.load(albums_json)["albums"]

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

        album_data.append({
            "src": src_value,
            "url": href_value,
            "title": "Album Title"
        })

    print("Bandcamp albums were not cached :(")
    return album_data

