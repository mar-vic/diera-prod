from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register  # register the application
class PhotologueApphook(CMSApp):
    app_name = "photologue"
    name = "Galleries"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["photologue_cms_integration.urls"]
        # return ["photologue.urls"]
