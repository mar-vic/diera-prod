from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _

from .models import FestivalProgramming

@plugin_pool.register_plugin
class FestivalProgrammingPlugin(CMSPluginBase):
    model = FestivalProgramming
    render_template = "festival_programming_plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
