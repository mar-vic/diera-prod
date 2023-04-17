from datetime import datetime as dt
import json

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import (
    gettext,
    gettext_lazy as _,
)

from cms.models import Page
from cms.forms.wizards import CreateCMSPageForm, CreateCMSSubPageForm
from cms.utils.page_permissions import (
    user_can_add_page,
    user_can_add_subpage,
)
from djangocms_text_ckeditor.fields import HTMLField

from filer.models import File
from filer.models.foldermodels import Folder

from .widgets import MonthYearSelectorWidget
from . import queries


class CreateArticleWizardForm(CreateCMSSubPageForm):
    def get_template(self):
        """This sets the template for articles."""
        return 'featured_article.html'

    def clean_parent_node(self):
        # Check to see if this user has permissions to make this page. We've
        # already checked this when producing a list of wizard entries, but this
        # is to prevent people from possible form-hacking.
        if self.page and self.sub_page_form:
            # User is adding a page which will be a direct
            # child of the current page.


            # Articles 'live' under homepage
            parent_page = Page.objects.filter(reverse_id='home').filter(publisher_is_draft=False).first()


        elif self.page and self.page.parent_page:
            # User is adding a page which will be a right
            # sibling to the current page.
            parent_page = self.page.parent_page
        else:
            parent_page = None

        if parent_page:
            has_perm = user_can_add_subpage(self.user, target=parent_page)
        else:
            has_perm = user_can_add_page(self.user)

        if not has_perm:
            message = gettext('You don\'t have the permissions required to add a page.')
            raise ValidationError(message)
        return parent_page.node if parent_page else None


class CreateEventWizardForm(CreateCMSSubPageForm):
    def get_template(self):
        """This sets the template for articles."""
        return 'event.html'

    def clean_parent_node(self):
        # Check to see if this user has permissions to make this page. We've
        # already checked this when producing a list of wizard entries, but this
        # is to prevent people from possible form-hacking.
        if self.page and self.sub_page_form:
            # User is adding a page which will be a direct
            # child of the current page.


            # Events 'live' under program
            parent_page = Page.objects.filter(reverse_id='program').filter(publisher_is_draft=False).first()


        elif self.page and self.page.parent_page:
            # User is adding a page which will be a right
            # sibling to the current page.
            parent_page = self.page.parent_page
        else:
            parent_page = None

        if parent_page:
            has_perm = user_can_add_subpage(self.user, target=parent_page)
        else:
            has_perm = user_can_add_page(self.user)

        if not has_perm:
            message = gettext('You don\'t have the permissions required to add a page.')
            raise ValidationError(message)
        return parent_page.node if parent_page else None


class CreateFestivalWizardForm(CreateCMSSubPageForm):
    def get_template(self):
        """This sets the template for articles."""
        return 'festival.html'

    def clean_parent_node(self):
        # Check to see if this user has permissions to make this page. We've
        # already checked this when producing a list of wizard entries, but this
        # is to prevent people from possible form-hacking.
        if self.page and self.sub_page_form:
            # User is adding a page which will be a direct
            # child of the current page.


            # Festivals 'live' under festivals.html
            parent_page = Page.objects.filter(reverse_id='festivals').filter(publisher_is_draft=False).first()


        elif self.page and self.page.parent_page:
            # User is adding a page which will be a right
            # sibling to the current page.
            parent_page = self.page.parent_page
        else:
            parent_page = None

        if parent_page:
            has_perm = user_can_add_subpage(self.user, target=parent_page)
        else:
            has_perm = user_can_add_page(self.user)

        if not has_perm:
            message = gettext('You don\'t have the permissions required to add a page.')
            raise ValidationError(message)
        return parent_page.node if parent_page else None



class CreateFestivalYearWizardForm(CreateCMSSubPageForm):
    festival = forms.ChoiceField(choices=queries.get_festival_choices(), label='Festival', help_text='This setting associates the page with selected festival.', required=True)

    def get_template(self):
        """This sets the template for festival year page."""
        return 'festival_year.html'

    def clean(self):
        """Set the parent page on the basis of what is selected in the 'festival' ChoiceField."""
        super().clean()
        new_cleaned_data = self.cleaned_data
        parent_page_id = self.cleaned_data['festival']
        parent_page = Page.objects.filter(id=parent_page_id).filter(publisher_is_draft=False).first()
        new_cleaned_data['parent_node'] = parent_page.node
        return new_cleaned_data


    # def clean_parent_node(self):
        # Check to see if this user has permissions to make this page. We've
        # already checked this when producing a list of wizard entries, but this
        # is to prevent people from possible form-hacking.
        # if self.page and self.sub_page_form:
            # User is adding a page which will be a direct
            # child of the current page.


            # Festival year 'live' under selected festival page
            # self.is_valid()
            # self.clean_festival()
            # parent_page_id = self.cleaned_data['festival']
            # parent_page = Page.objects.filter(id=parent_page_id).filter(publisher_is_draft=False).first()


        # elif self.page and self.page.parent_page:
            # User is adding a page which will be a right
            # sibling to the current page.
            # parent_page = self.page.parent_page
        # else:
        #     parent_page = None

        # if parent_page:
        #     has_perm = user_can_add_subpage(self.user, target=parent_page)
        # else:
        #     has_perm = user_can_add_page(self.user)

        # if not has_perm:
        #     message = gettext('You don\'t have the permissions required to add a page.')
        #     raise ValidationError(message)
        # return parent_page.node if parent_page else None


class SetBackgroundImageWizardForm(forms.Form):
    file = forms.FileField(label='Background Image File')
    month_year = forms.DateField(label='Schedule Background For Month/Year', help_text='The information is used to decide when the image is supposed to be set as sites background.', widget=MonthYearSelectorWidget)

    def save(self):
        ffile = File.objects.create()
        ffile.file = self.cleaned_data['file']
        ffile.folder = Folder.objects.filter(name='background_images').first()
        ffname = str(self.cleaned_data['month_year'].year) + '_' + str(self.cleaned_data['month_year'].month)
        ffile.name = ffname

        # If there is already an image scheduled for given date, delete it
        previous_backgrounds = File.objects.filter(folder__name='background_images').filter(name=ffname)
        for background in previous_backgrounds:
            background.delete()

        ffile.save()
        return ffile


class SetOpeningHoursWizardForm(forms.Form):
    customOpeningHoursFlag = forms.BooleanField(label='Custom hours',
                                                help_text='Check the box if you want to set the opening hours manually',
                                                required=False)
    openingHours = forms.TimeField(label='Opening Hours', required=False)

    def save(self):
        with open('static/opening_hours.json', 'w+') as openingHoursFile:
            data = {
                'customHours': self.cleaned_data['customOpeningHoursFlag'],
                'openingHours': self.cleaned_data['openingHours'].isoformat()
            }
            json.dump(data, openingHoursFile)
