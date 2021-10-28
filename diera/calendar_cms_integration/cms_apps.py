from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register  # register the application
class EventCalendarApphook(CMSApp):
    app_name = "event_calendar"
    name = "Calendar Application"

    def get_urls(self, page=None, language=None, **kwargs):
        return ["event_calendar.urls"]
