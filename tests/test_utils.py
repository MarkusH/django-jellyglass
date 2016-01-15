from django.test import RequestFactory, TestCase, override_settings
from django.views.debug import CLEANSED_SUBSTITUTE

from jellyglass.models import Spoon
from jellyglass.utils import record_spoon


class SensitivePostParametersTest(TestCase):

    def setUp(self):
        rf = RequestFactory()
        self.request = rf.post('/post/', data={
            'insecure': 'insecure value',
            'secure': 'secure value',
        })

    def test_disabled_none(self):
        @record_spoon('Jelly', post_fields='__ALL__', sensitive=None)
        def view(request):
            pass

        view(self.request)

        spoon = Spoon.objects.first()
        self.assertJSONEqual(spoon.post, {
            'insecure': 'insecure value',
            'secure': 'secure value',
        })

    def test_disabled_empty(self):
        @record_spoon('Jelly', post_fields='__ALL__', sensitive=[])
        def view(request):
            pass

        view(self.request)

        spoon = Spoon.objects.first()
        self.assertJSONEqual(spoon.post, {
            'insecure': 'insecure value',
            'secure': 'secure value',
        })

    def test_disabled_secure(self):
        @record_spoon('Jelly', post_fields='__ALL__', sensitive=['secure'])
        def view(request):
            pass

        view(self.request)

        spoon = Spoon.objects.first()
        self.assertJSONEqual(spoon.post, {
            'insecure': 'insecure value',
            'secure': 'secure value',
        })

    @override_settings(JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS=True)
    def test_enabled_none(self):
        @record_spoon('Jelly', post_fields='__ALL__', sensitive=None)
        def view(request):
            pass

        view(self.request)

        spoon = Spoon.objects.first()
        self.assertJSONEqual(spoon.post, {
            'insecure': 'insecure value',
            'secure': 'secure value',
        })

    @override_settings(JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS=True)
    def test_enabled_empty(self):
        @record_spoon('Jelly', post_fields='__ALL__', sensitive=[])
        def view(request):
            pass

        view(self.request)

        spoon = Spoon.objects.first()
        self.assertJSONEqual(spoon.post, {
            'insecure': CLEANSED_SUBSTITUTE,
            'secure': CLEANSED_SUBSTITUTE,
        })

    @override_settings(JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS=True)
    def test_enabled_secure(self):
        @record_spoon('Jelly', post_fields='__ALL__', sensitive=['secure'])
        def view(request):
            pass

        view(self.request)

        spoon = Spoon.objects.first()
        self.assertJSONEqual(spoon.post, {
            'insecure': 'insecure value',
            'secure': CLEANSED_SUBSTITUTE,
        })

    @override_settings(JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS=True)
    def test_enabled_no_secure(self):
        @record_spoon('Jelly', post_fields='__ALL__', sensitive=['secure'])
        def view(request):
            pass

        request = RequestFactory().post('/post/', data={
            'insecure': 'insecure value',
        })
        view(request)

        spoon = Spoon.objects.first()
        self.assertJSONEqual(spoon.post, {
            'insecure': 'insecure value',
        })
