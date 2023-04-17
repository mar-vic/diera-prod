from cms.models import Page
from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool

from .forms import (
    CreateArticleWizardForm,
    CreateEventWizardForm,
    CreateFestivalWizardForm,
    CreateFestivalYearWizardForm,
    SetBackgroundImageWizardForm,
    SetOpeningHoursWizardForm
)

from filer.models import File

class CreateArticleWizard(Wizard):
    pass



class CreateEventWizard(Wizard):
    pass



class CreateFestivalWizard(Wizard):
    pass



class CreateFestivalYearWizard(Wizard):
    pass



class SetBackgroundImageWizard(Wizard):
    def get_success_url(self, obj, **kwargs):
        """
        This should return the URL of the created object, «obj».
        """
        page = Page.objects.filter(reverse_id='home').filter(publisher_is_draft=False).first()

        if 'language' in kwargs:
            url = page.get_absolute_url()
        else:
            url = page.get_absolute_url()

        return url



class SetOpeningHoursWizard(Wizard):
    def get_success_url(self, obj, **kwargs):
        """
        Setting opening hours should redirect editor to the home page, since
        this is the only place where thery are shown.
        """
        page = Page.objects.filter(reverse_id='home').filter(publisher_is_draft=False).first()
        return page.get_absolute_url()



event_wizard = CreateEventWizard(
    title="New Event",
    weight=0,
    form=CreateEventWizardForm,
    description="Create a new Event",
)

article_wizard = CreateArticleWizard(
    title="New Article",
    weight=1,
    form=CreateArticleWizardForm,
    description="Create a new Article",
)

festival_wizard = CreateFestivalWizard(
    title="New Festival",
    weight=2,
    form=CreateFestivalWizardForm,
    description="Create a new Festival",
)

festival_year_wizard = CreateFestivalYearWizard(
    title="New Festival Year",
    weight=3,
    form=CreateFestivalYearWizardForm,
    description="Create a new festival year",
)

bgimage_wizard = SetBackgroundImageWizard(
    title="New Background Image",
    weight=3,
    form=SetBackgroundImageWizardForm,
    model=File,
    description="Set new background image"
)

hours_wizard = SetOpeningHoursWizard(
    title="Opening Hours",
    weight=3,
    form=SetOpeningHoursWizardForm,
    model=File,
    description="Set opening hours"
)

# Unregister default DjangoCMS wizard
for wizard in wizard_pool.get_entries():
    wizard_pool.unregister(wizard)

# Register wizards for Diera editors
wizard_pool.register(event_wizard)
wizard_pool.register(article_wizard)
wizard_pool.register(festival_wizard)
wizard_pool.register(festival_year_wizard)
wizard_pool.register(bgimage_wizard)
wizard_pool.register(hours_wizard)
