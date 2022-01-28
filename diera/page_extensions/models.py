from datetime import datetime as dt
from django.db import models
from django.core.exceptions import ValidationError

from cms.extensions import PageExtension, TitleExtension
from cms.extensions.extension_pool import extension_pool
from cms.models.pagemodel import Page
from djangocms_text_ckeditor.fields import HTMLField

from filer.fields.image import FilerImageField


# Page Extensions (language independent)
class FeaturedExtension(PageExtension):
    class Meta:
        verbose_name = "Featured"

    """
    Boolean field used to feature events on the homepage.
    """
    featured = models.BooleanField("Featured", help_text="Check, if the event is supposed to be featured on the homepage", default=False)


class TeaserImageExtension(PageExtension):
    class Meta:
        verbose_name = "Teaser Image"

    """
    Image to be shown in teaser boxes of articles, events and festivals.
    It is a extension of page, since it is language independent.
    """
    teaser_image = models.ImageField(default='default_teaser_image.jpeg', upload_to='teaser_images/')
    # teaser_image = FilerImageField(null=True,
    #                                blank=True,
    #                                related_name="teaser_image")

class ImageExtension(PageExtension):
    class Meta:
        verbose_name = "Page Image"

    """
    Image to be shown in teaser boxes of articles, events and fesitvals.
    It is an extension of Page model, since it is language independent.
    """
    image = FilerImageField(null=True,
                            blank=True,
                            related_name="teaser_image",
                            on_delete=models.CASCADE)


class EventDataExtension(PageExtension):
    class Meta:
        verbose_name = "Event Scheduling"

    # Event duration
    date_from = models.DateTimeField("FROM", help_text="Starting date of the event. (has to be set in order for event to show in the calendar)", blank=True, null=True)
    date_to = models.DateField("TO", help_text="Finishing date for recurring events. (the date is inclusive, so, in case of one day events, it should be equal to the starting date of the event or left blank)", blank=True, null=True)

    # Reference to the festival the event is supposed to be a part of.
    # Event can be associated with no festival.
    festival = models.ForeignKey(
        Page,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name='parent_festival',
        help_text="If the event is part of a festival, select one. Otherwise, leave unset. (the information is used to generate festival programs and parts of calendar)",
    )

    # Validation
    def clean(self):
        # Finishing date cannot be set when starting date is not set
        if self.date_to and not self.date_from:
            raise ValidationError('Finishing date cannot be set if starting date is not set.')
        # Don't allow event finishing date to precede its starting date
        if self.date_from and self.date_to and self.date_to < self.date_from.date():
            raise ValidationError('Finishing date cannot precede starting date.')


class FestivalYearExtension(PageExtension):
    """
    Festival year pages need to store the information about the year of the
    festival they are supposed to represent, since the information is used to
    generate the programming for the festival in given year.
    """
    class Meta:
        verbose_name = "Festival year"

    festival_year = models.DecimalField(max_digits=4, decimal_places=0, default=dt.now().year)


# extension_pool.register(ArticleExtension)
extension_pool.register(ImageExtension)
extension_pool.register(TeaserImageExtension)
extension_pool.register(EventDataExtension)
extension_pool.register(FeaturedExtension)
extension_pool.register(FestivalYearExtension)


# Title Extensions (language dependent)
class TeaserTextExtension(TitleExtension):
    class Meta:
        verbose_name = "Teaser Text"

    """Text to be shown in teaser boxes of articles, events and festivals."""
    teaser_text = HTMLField(blank=True)


extension_pool.register(TeaserTextExtension)
