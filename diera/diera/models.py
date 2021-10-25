from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin

from django.db import models

# def limit_choices_to_festivals():
#     return {'id': Page.objects.filter(reverse_id='festivals').filter(publisher_is_draft=False)[0].get_child_pages()}


# class FestivalProgramming(CMSPlugin):
    # festival_name = models.CharField(max_length=50, default='BlaBla')
    # festival = models.ForeignKey(
    #     Page,
    #     models.SET_NULL,  # The key is nullable
    #     blank=True,
    #     null=True,  # Will set the key on null when referenced object is deleted
    #     limit_choices_to={'title': 'Mobilis'}
    # )
    # festival = models.CharField(max_length=50, default="Festival")
    # year = models.IntegerField(default=2021)

