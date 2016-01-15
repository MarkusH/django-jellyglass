from django.test import RequestFactory, TestCase

from jellyglass.models import Spoon


class SpoonTest(TestCase):

    def test_all_get_fields(self):
        rf = RequestFactory()
        url = '/login/?validgetkey1=validgetdata1&validgetkey2=validgetdata2'
        request = rf.post(url, {
            'validpostkey': 'validpostdata',
            'invalidpostkey': 'invalidpostdata',
        })
        spoon = Spoon.from_request(
            request, 'Something',
            get_fields='__ALL__', post_fields=['validpostkey'],
        )
        self.assertEqual(spoon.jelly, 'Something')
        self.assertEqual(spoon.url, 'http://testserver' + url)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, 'N/A')
        self.assertEqual(spoon.user_agent, 'N/A')
        self.assertJSONEqual(spoon.get, {
            'validgetkey1': 'validgetdata1',
            'validgetkey2': 'validgetdata2'
        })
        self.assertJSONEqual(spoon.post, {
            'validpostkey': 'validpostdata',
        })

    def test_all_post_fields(self):
        rf = RequestFactory()
        url = '/login/?validgetkey=validgetdata&invalidgetkey=invalidgetdata'
        request = rf.post(url, {
            'validpostkey1': 'validpostdata1',
            'validpostkey2': 'validpostdata2',
        })
        spoon = Spoon.from_request(
            request, 'Something',
            get_fields=['validgetkey'], post_fields='__ALL__',
        )
        self.assertEqual(spoon.jelly, 'Something')
        self.assertEqual(spoon.url, 'http://testserver' + url)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, 'N/A')
        self.assertEqual(spoon.user_agent, 'N/A')
        self.assertJSONEqual(spoon.get, {
            'validgetkey': 'validgetdata',
        })
        self.assertJSONEqual(spoon.post, {
            'validpostkey1': 'validpostdata1',
            'validpostkey2': 'validpostdata2'
        })
