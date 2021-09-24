"""sample implementations for IntegrationPlugin"""
from plugins.integration.integration import SettingsMixin, UrlsMixin, NavigationMixin, IntegrationPlugin

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url, include


class SampleIntegrationPlugin(SettingsMixin, UrlsMixin, NavigationMixin, IntegrationPlugin):
    """
    An full integration plugin
    """

    PLUGIN_NAME = "SampleIntegrationPlugin"

    def view_test(self, request):
        """very basic view"""
        return HttpResponse(f'Hi there {request.user.username} this works')

    def setup_urls(self):
        he = [
            url(r'^he/', self.view_test, name='he'),
            url(r'^ha/', self.view_test, name='ha'),
        ]

        return [
            url(r'^hi/', self.view_test, name='hi'),
            url(r'^ho/', include(he), name='ho'),
        ]

    SETTINGS = {
        'PO_FUNCTION_ENABLE': {
            'name': _('Enable PO'),
            'description': _('Enable PO functionality in InvenTree interface'),
            'default': True,
            'validator': bool,
        },
    }

    NAVIGATION = [
        {'name': 'SampleIntegration', 'link': 'plugin:SampleIntegrationPlugin:hi'},
    ]
