from operator import itemgetter
import datetime
from datetime import date

from django import template
from django.core.exceptions import ObjectDoesNotExist

from cms.models import Page
from photologue.models import Gallery, Photo
from filer.models.filemodels import File
from filer.models.foldermodels import Folder

register = template.Library()

@register.simple_tag
def get_years_with_galleries_added():
    years = set()
    for gallery in Gallery.objects.filter(is_public=True):
        years.add(gallery.date_added.year)
    return [str(year) for year in sorted(list(years), reverse=True)]

@register.inclusion_tag('photologue/includes/gallery_slider.html')
def gallery_slider(gallery):
    return {'gallery': gallery}

@register.inclusion_tag('photologue/includes/gallery_slider_nh.html')
def gallery_slider_nh(slug):
    gallery = Gallery.objects.filter(slug=slug).first()
    return {'gallery': gallery}

@register.inclusion_tag('photologue/includes/meet_the_team.html')
def meet_the_team():
    return

@register.simple_tag
def get_photo_by_slug(slug):
    return Photo.objects.get(slug=slug)

@register.simple_tag
def get_teasers_for_festival_years(request):
    """
    Return teasers for festival year pages.
    """
    language = request.LANGUAGE_CODE

    # Ensure that we have a festival page
    festival_page = request.current_page
    parent_page = festival_page.get_parent_page()
    if not parent_page or not parent_page.reverse_id == 'festivals':
        return []

    # Get all festival year pages
    festival_year_pages = [page for page in festival_page.get_child_pages() if page.is_published(language)]

    # Generate teasers for festival year pages
    teasers = []

    for page in festival_year_pages:
        # Ensuring that extensions were initialized
        try:
            teaser_image = page.imageextension.image
        except ObjectDoesNotExist:
            teaser_image = None

        try:
            festival_year = page.festivalyearextension.festival_year
        except ObjectDoesNotExist:
            continue

        teasers.append(
                {
                    'url': page.get_absolute_url(),
                    'title': page.get_page_title(),
                    'page_id': page.id,
                    'image': teaser_image,
                    'year': festival_year,
                }
        )

    return teasers

    # while festival_year_pages:
    #     teaser_triplet = []
    #     for page in festival_year_pages[0:3]:

    #         # Ensuring that extensions were initialized
    #         try:
    #             teaser_image = page.imageextension.image
    #         except ObjectDoesNotExist:
    #             teaser_image = None

    #         try:
    #             festival_year = page.festivalyearextension.festival_year
    #         except ObjectDoesNotExist:
    #             continue

    #         teaser_triplet.append(
    #             {
    #                 'url': page.get_absolute_url(),
    #                 'title': page.get_page_title(),
    #                 'page_id': page.id,
    #                 'image': teaser_image,
    #                 'year': festival_year,
    #             }
    #         )

    #     teasers.append(teaser_triplet)
    #     festival_year_pages = festival_year_pages[3:]

    # return teasers


@register.simple_tag
def get_teasers_for_festival_events(request, festival_name, year):
    """
    Return all teasers for events of a festival.
    """
    language = request.LANGUAGE_CODE

    # Get all published events
    programp = [page for page in Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False) if page.is_published(language) and page][0]
    published_events = [page for page in programp.get_child_pages() if page.is_published(language)]

    # Generate list of event teasers
    event_teasers = []

    for event in published_events:
        teaser = {}

        try:
            teaser_image = event.imageextension.image
        except ObjectDoesNotExist:
            teaser_image = None

        # Extension objects have to be manualy set in order to exist. Skip all
        # unscheduled events
        try:
            date_from = event.eventdataextension.date_from
            date_to = event.eventdataextension.date_to
            festival = event.eventdataextension.festival
        except ObjectDoesNotExist:
            continue

        # Do not create a teaser if the event is not a part of given festival
        # or have not taken the place at given year
        if (
                not festival or
                str.lower(festival_name) != str.lower(festival.get_page_title()) or
                date_from.year != year
        ):
            continue

        teaser['url'] = event.get_absolute_url()
        teaser['title'] = event.get_page_title()
        teaser['page_id'] = event.id
        teaser['image'] = teaser_image
        teaser['from'] = date_from
        teaser['to'] = date_to
        teaser['festival'] = festival

        event_teasers.append(teaser)

    # Sort event teasers by by their scheduling in ascending order
    event_teasers = sorted(event_teasers,
                  key=lambda teaser: teaser['from'],
                           reverse=False)
    event_teasers_triplets = []
    while event_teasers:
        event_teasers_triplets.append(event_teasers[0:3])
        event_teasers = event_teasers[3:]

    return event_teasers_triplets

@register.simple_tag
def get_teasers_for_all_features(request):
    """
    Return all teasers that will be featured on homepage. There two types of
    teasers: article teasers (ie, teasers for homepage childs) and event teasers
    (ie, teasers for program childs).
    """

    # DEBUGING
    # import pdb; pdb.set_trace()

    language = request.LANGUAGE_CODE

    # Get the home page (ie, page with reverse_id='home')
    homep = Page.objects.filter(reverse_id='home').filter(publisher_is_draft=False).first()
    # Ensuring that homepage does exist
    if not homep:
        return []
    else:
        # Get all childs of homepage (i.e., the articles)
        published_articles = [page for page in homep.get_child_pages().order_by('-publication_date') if page.is_published(language)]

    # Get the program page (i.e., page with reverse_id='program')
    programp = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False).first()
    # Ensuring that program page does exist
    if not programp:
        published_events = []
    else:
        # Get all childs of program page (i.e., the events)
        published_events = [page for page in programp.get_child_pages() if page.is_published(language)]

    # Generate list of article teasers
    article_teasers = []

    for article in published_articles:
        teaser = {}

        # Extension objects have to be manually set in order to exist
        try:
            teaser_image = article.imageextension.image
        except ObjectDoesNotExist:
            teaser_image = None

        teaser['url'] = article.get_absolute_url()
        teaser['title'] = article.get_page_title()
        teaser['image'] = teaser_image
        teaser['page_id'] = article.id

        article_teasers.append(teaser)

    # Generate list of event teasers
    event_teasers = []

    for event in published_events:
        teaser = {}

        try:
            teaser_image = event.imageextension.image
        except ObjectDoesNotExist:
            teaser_image = None

        # Extension objects have to be manualy set in order to exist. Skip all
        # unscheduled (and unfeatured) events
        try:
            date_from = event.eventdataextension.date_from
            date_to = event.eventdataextension.date_to
            festival = event.eventdataextension.festival
            featured = event.featuredextension.featured
        except ObjectDoesNotExist:
            continue

        # Skip unfeatured or passed featured events
        delta_from = (date_from - datetime.datetime.now(datetime.timezone.utc)).days

        if not featured:
            continue
        elif delta_from < 0:
            continue
        elif date_to and (date_to - date.today()).days < 0:
            continue

        teaser['url'] = event.get_absolute_url()
        teaser['title'] = event.get_page_title()
        teaser['page_id'] = event.id
        teaser['image'] = teaser_image
        teaser['from'] = date_from
        teaser['to'] = date_to
        teaser['festival'] = festival

        event_teasers.append(teaser)

    # Sort event teasers by their scheduling in ascending order
    event_teasers = sorted(event_teasers,
                           key=lambda teaser: teaser['from'],
                           reverse=True)

    # Get festivals page (ie, page with reverse_id='festivals')
    festivalsp = Page.objects.filter(reverse_id='festivals').filter(publisher_is_draft=False).first()
    festival_teasers = []

    # Generate teasers for festival pages and their year pages as
    for festival_page in festivalsp.get_child_pages():

        # Extension objects have to manualy set in order to exist.
        try:
            teaser_image = festival_page.imageextension.image
        except ObjectDoesNotExist:
            teaser_image = None

        # Extension objects have to be manualy set in order to exist. Skip all
        # unscheduled (and unfeatured) events
        try:
            featured = festival_page.featuredextension.featured
        except ObjectDoesNotExist:
            continue

        # Append teaser if festival is featured
        if featured:
            festival_teasers.append(
                {
                    'url' : festival_page.get_absolute_url(),
                    'title' : festival_page.get_page_title(),
                    'image' : teaser_image,
                    'page_id' : festival_page.id,
                }
            )

        # Check for featured festival year pages
        for festival_year_page in festival_page.get_child_pages():
            # Extension objects have to manualy set in order to exist.
            try:
                teaser_image = festival_year_page.imageextension.image
            except ObjectDoesNotExist:
                teaser_image = None

            # Extension objects have to be manualy set in order to exist. Skip all
            # unscheduled (and unfeatured) events
            try:
                featured = festival_year_page.featuredextension.featured
            except ObjectDoesNotExist:
                continue

            if featured:
                festival_teasers.append(
                    {
                        'url' : festival_year_page.get_absolute_url(),
                        'title' : festival_year_page.get_page_title(),
                        'image' : teaser_image,
                        'page_id' : festival_year_page.id,
                    }
                )

    # Create a teaser for newsletter page
    newsletterp = Page.objects.filter(reverse_id='newsletter').filter(publisher_is_draft=False).first()
    newsletter_teaser = []

    if newsletterp and language == 'sk':
        # Extension objects have to manualy set in order to exist.
        try:
            teaser_image = newsletterp.imageextension.image
        except ObjectDoesNotExist:
            teaser_image = None

        newsletter_teaser = [
            {
                'url' : newsletterp.get_absolute_url(),
                'title' : newsletterp.get_page_title(),
                'image' : teaser_image,
                'page_id' : newsletterp.id,
            }
        ]

    # First init teasers with festival teasers
    teasers = festival_teasers

    # Merge event and article teasers lists in alternating order
    while(event_teasers):
        teasers.append(event_teasers.pop())
        if article_teasers:
            teasers.append(article_teasers.pop())


    # While returning teasers, append yet unpopped article teasers, and, finally, a teaser for the newsletter page
    return teasers + article_teasers + newsletter_teaser
    # return festival_teasers + event_teasers + article_teasers


@register.simple_tag
def get_festival_teasers(request):
    language = request.LANGUAGE_CODE
    homep = [page for page in Page.objects.filter(reverse_id='festivals').filter(publisher_is_draft=False) if page.is_published(language) and page][0]
    festivals = [page for page in homep.get_child_pages().order_by('publication_date') if page.is_published(language)]
    teasers = []

    for festival in festivals:
        teaser = {}

        # Extension objects have to be manualy set in order to exist, so use
        # default values, if they were not yet set
        try:  # teaser image exception handling
            teaser_image = festival.imageextension.image
        except ObjectDoesNotExist:
            teaser_image = None

        try:  # teaser text exception handling
            teaser_text = festival.get_title_obj().teasertextextension.teaser_text
        except ObjectDoesNotExist:
            teaser_text = "<b>Write your teaser text through the 'Festival Settings -> Teaser Text...' menu in toolbar.</b>"

        teaser['url'] = festival.get_absolute_url()
        teaser['title'] = festival.get_page_title()
        teaser['text'] = teaser_text
        teaser['image'] = teaser_image
        teaser['page_id'] = festival.id

        teasers.append(teaser)

    return teasers

@register.simple_tag
def get_scheduling_for_page(page):
    try:
        date_from = page.eventdataextension.date_from
        date_to = page.eventdataextension.date_to
    except ObjectDoesNotExist:
        return None

    return {'date_from': date_from, 'date_to': date_to}

@register.simple_tag
def get_festival_years():
    """
    Return years in which festival was organized. This is determined by date of
    events subsumed under given festival.
    """

    return [2021, 2020, 2019]

@register.simple_tag
def get_festival_programming(festival_id):
    """
    Return programming for a given festival.
    """

    # Select the parent page of all event pages
    programming_page = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False).first()

    # Select all event pages
    all_event_pages = programming_page.get_child_pages().filter(publisher_is_draft=False)

    # Select all event pages flagged as part the festival and populate the keys in programming dictionary
    festival_event_pages = []
    festival_programming = {}
    for page in all_event_pages:
        if page.eventdataextension.festival_id == festival_id:
            eteaser = {}
            festival_event_pages.append(page)
            festival_programming[page.eventdataextension.date_from.year] = []

    # Sort events by their scheduling
    festival_event_pages = sorted(
        festival_event_pages,
        key=lambda event_page: event_page.eventdataextension.date_from,
        reverse=True
    )

    # Generate the values in programming dictionary
    for event_page in festival_event_pages:
        event_date = event_page.eventdataextension.date_from.year
        festival_programming[event_date].append(event_page)

    return {
        'festival_programming': festival_programming,
        'festival_years': list(festival_programming.keys())
    }

@register.simple_tag
def get_background_image_url():
    """
    Return the url of an image to be used as site background from the
    'background_images' folder. The image is chosen according to following rules:
    1) return image named 'current'; 2) otherwise return image named '<current
    year>_<current_month>; 3) otherwise return the url of last uploaded image;
    4) finally, if there is no image in the folder, return empty string, thus
    making the site with haveing no background image.
    """
    today = date.today()

    # Try to get folder with background images and fail gracefully when it does not exist.
    try:
        folder = Folder.objects.get(name='background_images')
    except ObjectDoesNotExist:
        return ''

    bgimage_by_flag = folder.files.filter(name='current').first()
    bgimage_by_date = folder.files.filter(name=f"{today.year}_{today.month}").first()
    bgimage_by_uploaded = folder.files.order_by('-uploaded_at').first()

    if bgimage_by_flag:
        return bgimage_by_flag.url
    elif bgimage_by_date:
        return bgimage_by_date.url
    elif bgimage_by_uploaded:
        return bgimage_by_uploaded.url
    else:
        return ''
