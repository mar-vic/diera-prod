from django.contrib import admin

from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin
from cms.models import Page

from .models import ImageExtension, TeaserImageExtension, TeaserTextExtension, EventDataExtension, FeaturedExtension

class ImageExtensionAdmin(PageExtensionAdmin):
    pass

class TeaserImageExtensionAdmin(PageExtensionAdmin):
    pass


class TeaserTextExtensionAdmin(TitleExtensionAdmin):
    pass


class EventDataExtensionAdmin(PageExtensionAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit the selection of festivals to the subpages of 'Festivals' page."""
        if db_field.name == "festival":
            kwargs["queryset"] = Page.objects.filter(reverse_id='festivals').filter(publisher_is_draft=False)[0].get_child_pages()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class FeaturedExtensionAdmin(PageExtensionAdmin):
    pass


admin.site.register(ImageExtension, ImageExtensionAdmin)
admin.site.register(TeaserImageExtension, TeaserImageExtensionAdmin)
admin.site.register(TeaserTextExtension, TeaserTextExtensionAdmin)
admin.site.register(EventDataExtension, EventDataExtensionAdmin)
admin.site.register(FeaturedExtension, FeaturedExtensionAdmin)
