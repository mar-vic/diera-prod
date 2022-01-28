from django.utils.translation import gettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils import get_language_list

from .models import (
    ImageExtension,
    TeaserImageExtension,
    TeaserTextExtension,
    EventDataExtension,
    FeaturedExtension,
    FestivalYearExtension
)

@toolbar_pool.register
class ImageExtensionToolbar(ExtensionToolbar):
    model = ImageExtension

    def populate(self):

        verbose_name = None

        try:
            cur_page_parent = self.request.current_page.get_parent_page()
        except AttributeError:
            return

        if not cur_page_parent or cur_page_parent.reverse_id not in ['home', 'program', 'festivals']:
            # Try for festival years
            try:
                cur_page_parent = self.request.current_page.get_parent_page().get_parent_page()
            except AttributeError:
                return

            if not cur_page_parent or cur_page_parent.reverse_id != 'festivals':
                return
            else:
                verbose_name = 'Festival Year Settings'

        parent_id = cur_page_parent.reverse_id
        verbose_name = verbose_name if verbose_name else 'Article Settings' if parent_id == 'home' else 'Event Settings' if parent_id == 'program' else 'Festival Settings'

        menu = self.toolbar.get_or_create_menu(
            key='page_extensions_menu',
            verbose_name=verbose_name
        )

        if menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                # adds a toolbar in position 0 (at the top of the menu)
                menu.add_modal_item(_('Teaser Image'), url=url,
                                    disabled=not self.toolbar.edit_mode_active, position=0)


# @toolbar_pool.register
# class TeaserImageExtensionToolbar(ExtensionToolbar):
#     # defines the model for the current toolbar
#     model = TeaserImageExtension

#     def populate(self):

#         try:
#             cur_page_parent = self.request.current_page.get_parent_page()
#         except AttributeError:
#             return

#         if not cur_page_parent or cur_page_parent.reverse_id not in ['home', 'program', 'festivals']:
#             return

#         parent_id = cur_page_parent.reverse_id
#         verbose_name = 'Article Settings' if parent_id == 'home' else 'Event Settings' if parent_id == 'program' else 'Festival Settings'

#         menu = self.toolbar.get_or_create_menu(
#             key='page_extensions_menu',
#             verbose_name=verbose_name
#         )

#         if menu:
#             # retrieves the instance of the current extension (if any) and the toolbar item URL
#             page_extension, url = self.get_page_extension_admin()
#             if url:
#                 # adds a toolbar in position 0 (at the top of the menu)
#                 menu.add_modal_item(_('Teaser Image'), url=url,
#                                     disabled=not self.toolbar.edit_mode_active, position=0)


# @toolbar_pool.register
# class TeaserTextExtensionToolbar(ExtensionToolbar):
#     # defines the model for the current toolbar
#     model = TeaserTextExtension

#     def populate(self):

#         # Only subpages are supposed to have teasers
#         try:
#             cur_page_parent = self.request.current_page.get_parent_page()
#         except AttributeError:
#             return

#         # Only articles (subpages of 'home'), events (subs of 'program') or festivals (subs of 'festivals') are supposed to have teasers
#         if not cur_page_parent or cur_page_parent.reverse_id not in ['home', 'program', 'festivals']:
#             return

#         parent_id = cur_page_parent.reverse_id
#         verbose_name = 'Article Settings' if parent_id == 'home' else 'Event Settings' if parent_id == 'program' else 'Festival Settings'

#         menu = self.toolbar.get_or_create_menu(
#             key='page_extensions_menu',
#             verbose_name=verbose_name
#         )

#         if menu:
#             # retrieves the instance of the current extension (if any) and the toolbar item URL
#             page_extension, url = self.get_page_extension_admin()
#             if url:
#                 # adds a toolbar in position 0 (at the top of the menu)
#                 menu.add_modal_item(_('Teaser Text'), url=url,
#                                     disabled=not self.toolbar.edit_mode_active,position=1)

# @toolbar_pool.register
# class TeaserTextExtensionToolbar(ExtensionToolbar):
#     # defines the model for the current toolbar
#     model = TeaserTextExtension

#     def populate(self):

#         # Only subpages are supposed to have teasers
#         try:
#             cur_page_parent = self.request.current_page.get_parent_page()
#         except AttributeError:
#             return

#         # Only articles (subpages of 'home'), events (subs of 'program') or festivals (subs of 'festivals') are supposed to have teasers
#         if not cur_page_parent or cur_page_parent.reverse_id not in ['home', 'program', 'festivals']:
#             return

#         # The name of the menu item is determined by the parent
#         parent_id = cur_page_parent.reverse_id
#         verbose_name = 'Article Settings' if parent_id == 'home' else 'Event Settings' if parent_id == 'program' else 'Festival Settings'

#         # The name of extension menu depends on the parent of current page
#         parent_id = cur_page_parent.reverse_id
#         verbose_name = 'Article Settings' if parent_id == 'home' else 'Event Settings' if parent_id == 'program' else 'Festival Settings'

#         # Create the extension menu
#         extension_menu = self.toolbar.get_or_create_menu(
#             key='page_extensions_menu',
#             verbose_name=verbose_name
#         )

#         # if it's all ok
#         if extension_menu and self.toolbar.edit_mode_active:
#             # create sub menu for teaser text
#             sub_menu = self._get_sub_menu(
#                 extension_menu, 'sub_menu_label', 'Teaser Texts', position=1
#             )

#             # retrieves the instances of the current title extension (if any)
#             # and the toolbar item URL
#             urls = self.get_title_extension_admin()

#             # we also need to get titleset (i.e. different language titles)
#             # for this page
#             page = self._get_page()
#             titleset = page.title_set.filter(language__in=get_language_list(page.node.site_id))

#             # create a 3-tuple of (title_extension, url, title)
#             nodes = [(title_extension, url, title.title, title.language) for (
#                 (title_extension, url), title) in zip(urls, titleset)
#             ]

#             # cycle through the list of nodes
#             for title_extension, url, title, lan in nodes:
#                 language = 'English' if lan == 'en' else 'Slovak'

#                 # add toolbar items
#                 sub_menu.add_modal_item(
#                     "%s ('%s')" % (language, title), url=url, disabled=not self.toolbar.edit_mode_active
#                 )


@toolbar_pool.register
class EventDataExtensionToolbar(ExtensionToolbar):
    # defines the model for the current toolbar
    model = EventDataExtension

    def populate(self):
        try:
            cur_page_parent = self.request.current_page.get_parent_page()
        except AttributeError:
            return

        if not cur_page_parent or cur_page_parent.reverse_id != 'program':
            return

        verbose_name = 'Event Settings'

        menu = self.toolbar.get_or_create_menu(
            key='page_extensions_menu',
            verbose_name=verbose_name
        )

        if menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                menu.add_modal_item(_('Scheduling'), url=url,
                                    disabled=not self.toolbar.edit_mode_active, position=3)


@toolbar_pool.register
class FeaturedExtensionToolbar(ExtensionToolbar):
    model = FeaturedExtension

    def populate(self):
        verbose_name = None

        try:
            cur_page_parent = self.request.current_page.get_parent_page()
        except AttributeError:
            return

        if not cur_page_parent or cur_page_parent.reverse_id not in ['program', 'festivals']:
            # Try for festival years
            try:
                cur_page_parent = self.request.current_page.get_parent_page().get_parent_page()
            except AttributeError:
                return
            if not cur_page_parent or cur_page_parent.reverse_id != 'festivals':
                return
            else:
                verbose_name = 'Festival Year Settings'

        verbose_name = 'Festival Year Settings' if verbose_name else 'Event Settings' if cur_page_parent.reverse_id == 'program' else 'Festival Settings'

        menu = self.toolbar.get_or_create_menu(
            key='page_extensions_menu',
            verbose_name=verbose_name
        )

        if menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                menu.add_modal_item(_('Feature'), url=url,
                                    disabled=not self.toolbar.edit_mode_active, position=4)


@toolbar_pool.register
class FestivalYearExtensionToolbar(ExtensionToolbar):
    model = FestivalYearExtension

    def populate(self):
        try:
            cur_page_parent = self.request.current_page.get_parent_page().get_parent_page()
        except AttributeError:
            return

        if not cur_page_parent or cur_page_parent.reverse_id not in ['festivals']:
            return

        verbose_name = 'Festival Year Settings'

        menu = self.toolbar.get_or_create_menu(
            key='page_extensions_menu',
            verbose_name=verbose_name
        )

        if menu:
            # retrieves the instance of the current extension (if any) and the toolbar item URL
            page_extension, url = self.get_page_extension_admin()
            if url:
                menu.add_modal_item(_('Festival year'), url=url,
                                    disabled=not self.toolbar.edit_mode_active, position=4)
