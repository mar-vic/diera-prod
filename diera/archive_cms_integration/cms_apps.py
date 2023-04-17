from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register  # register the application
class ArchiveApphook(CMSApp):
    app_name = "archive"
    name = "Archive application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["archive.urls"]
