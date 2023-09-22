from datetime import date
import json
import requests

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
    teasers = []

    # Get the list of YT videos with API Request
    response  = requests.get("https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UC326HkT9w-FxK3ySvKfKxKQ&maxResults=100&order=date&key=AIzaSyCOCuuD2WnvEUCghSyh4cB6APdKAB67be4")

    # Generate the data for teasers
    for video in response.json()["items"]:
        if video["id"]["kind"] == "youtube#video":
            teaser = {}
            teaser["title"] = video["snippet"]["title"]
            teaser["description"] = video["snippet"]["description"]
            teaser["id"] = video["id"]["videoId"]
            teasers.append(teaser)

    # with open("static/diera_yt_videos.json", "r") as videos_json:
    #     data = json.load(videos_json)
    #     for video in data["items"]:
    #         if video["id"]["kind"] == "youtube#video":
    #             teaser = {}
    #             teaser["title"] = video["snippet"]["title"]
    #             teaser["description"] = video["snippet"]["description"]
    #             teaser["id"] = video["id"]["videoId"]
    #             teasers.append(teaser)

    # return [f"video {n}" for n in range(1, 100)]

    # print("Query has been run!")
    return teasers

def get_all_bandcamp_albums():
    with open("static/diera_bandcamp_albums.json", "r") as albums_json:
        return json.load(albums_json)["albums"]

