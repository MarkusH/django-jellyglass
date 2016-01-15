import json

from django.contrib import admin
from django.test import RequestFactory, TestCase

from jellyglass.admin import SpoonAdmin
from jellyglass.models import Spoon


class SpoonAdminTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.spoon = Spoon(
            jelly='Some Jelly',
            url='http://the.submit/path/url.php?include=query',
            remote_addr='1.2.3.4',
            referer='http://other.page/with/path/?and=querystring',
            user_agent='Some user agent',
            get=json.dumps({'some': 'query', 'more': 'value'}),
            post=json.dumps({'body': 'data', 'lorem': 'ipsum'}),
        )
        rf = RequestFactory()
        cls.request = rf.get('/admin/spoon/')
        cls.spoon_admin = SpoonAdmin(Spoon, admin.site)

    def test_regular_spoon(self):
        get_pretty = self.spoon_admin.get_pretty(self.spoon)
        self.assertHTMLEqual(get_pretty, """
            <dl style="margin-left: 170px">
                <dt>more</dt>
                <dd>value</dd>
                <dt>some</dt>
                <dd>query</dd>
            </dl>
        """)
        post_pretty = self.spoon_admin.post_pretty(self.spoon)
        self.assertHTMLEqual(post_pretty, """
            <dl style="margin-left: 170px">
                <dt>body</dt>
                <dd>data</dd>
                <dt>lorem</dt>
                <dd>ipsum</dd>
            </dl>
        """)

    def test_readonly_fields(self):
        fields = self.spoon_admin.get_readonly_fields(self.request, self.spoon)
        self.assertEqual(fields, [
            'id', 'jelly', 'accessed',
            'url', 'remote_addr', 'referer', 'user_agent',
            'get_pretty', 'post_pretty'
        ])
