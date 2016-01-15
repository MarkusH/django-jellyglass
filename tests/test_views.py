from django.core.urlresolvers import reverse
from django.test import TestCase

from jellyglass.models import Spoon


class JellyGlassDjangoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url_django_admin = reverse('jellyglass:django_admin')
        cls.url_django_admin_login = reverse('jellyglass:django_admin_login')

    def test_redirect_on_admin(self):
        response = self.client.get(self.url_django_admin, follow=True)
        to = self.url_django_admin_login + "?next=" + self.url_django_admin
        self.assertRedirects(response, to)

    def test_login_get(self):
        response = self.client.get(self.url_django_admin_login)
        self.assertContains(response, self.url_django_admin)
        self.assertContains(response, self.url_django_admin_login)
        self.assertTemplateUsed('jellyglass/django.html')

    def test_login_post(self):
        path = self.url_django_admin_login + '?next=/foo/'
        data = {
            'next': '/some-place/',
            'password': 'secret',
            'username': 'someone',
        }
        extra = {
            'HTTP_REFERER': 'http://somewhere.com/path/to?query=string',
            'HTTP_USER_AGENT': 'Django test client',
        }
        response = self.client.post(path, data=data, **extra)
        self.assertContains(response, self.url_django_admin)
        self.assertContains(response, self.url_django_admin_login)
        self.assertTemplateUsed('jellyglass/django.html')

        spoon = Spoon.objects.first()
        self.assertEqual(spoon.jelly, 'Django')
        self.assertEqual(spoon.url, 'http://testserver' + path)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, extra['HTTP_REFERER'])
        self.assertEqual(spoon.user_agent, extra['HTTP_USER_AGENT'])
        self.assertJSONEqual(spoon.get, {'next': '/foo/'})
        self.assertJSONEqual(spoon.post, data)

    def test_login_post_no_data(self):
        response = self.client.post(self.url_django_admin_login)
        self.assertContains(response, self.url_django_admin)
        self.assertContains(response, self.url_django_admin_login)
        self.assertTemplateUsed('jellyglass/django.html')

        spoon = Spoon.objects.first()
        self.assertEqual(spoon.jelly, 'Django')
        self.assertEqual(spoon.url, 'http://testserver' + self.url_django_admin_login)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, 'N/A')
        self.assertEqual(spoon.user_agent, 'N/A')
        self.assertJSONEqual(spoon.get, {'next': ''})
        self.assertJSONEqual(spoon.post, {
            'next': '',
            'password': '',
            'username': '',
        })

    def test_login_post_ignore_unused(self):
        path = self.url_django_admin_login + '?other=value'
        data = {
            'invalid': 'data',
        }
        response = self.client.post(path, data=data)
        self.assertContains(response, self.url_django_admin)
        self.assertContains(response, self.url_django_admin_login)
        self.assertTemplateUsed('jellyglass/django.html')

        spoon = Spoon.objects.first()
        self.assertEqual(spoon.jelly, 'Django')
        self.assertEqual(spoon.url, 'http://testserver' + path)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, 'N/A')
        self.assertEqual(spoon.user_agent, 'N/A')
        self.assertJSONEqual(spoon.get, {'next': ''})
        self.assertJSONEqual(spoon.post, {
            'next': '',
            'password': '',
            'username': '',
        })


class JellyGlassWordpressTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url_wordpress_admin = reverse('jellyglass:wordpress_admin')
        cls.url_wordpress_admin_login = reverse('jellyglass:wordpress_admin_login')

    def test_redirect_on_admin(self):
        response = self.client.get(self.url_wordpress_admin, follow=True)
        to = (
            'http://testserver' +
            self.url_wordpress_admin_login +
            '?redirect_to=http%3A%2F%2Ftestserver%2Fwp-admin%2F&reauth=1'
        )
        self.assertRedirects(response, to)

    def test_login_get(self):
        response = self.client.get(self.url_wordpress_admin_login)
        self.assertContains(response, self.url_wordpress_admin)
        self.assertContains(response, self.url_wordpress_admin_login)
        self.assertTemplateUsed('jellyglass/wordpress.html')

    def test_login_post(self):
        path = (
            self.url_wordpress_admin_login +
            '?redirect_to=http%3A%2F%2Ftestserver%2Fwp-admin%2F&reauth=1'
        )

        data = {
            'log': 'somebody',
            'pwd': 'secret',
            'redirect_to': '/somewhere/',
            'rememberme': 'yes',
            'testcookie': 'chocolate',
            'wp-submit': 'button'
        }
        extra = {
            'HTTP_REFERER': 'http://somewhere.com/path/to?query=string',
            'HTTP_USER_AGENT': 'Django test client',
        }
        response = self.client.post(path, data=data, **extra)
        self.assertContains(response, self.url_wordpress_admin)
        self.assertContains(response, self.url_wordpress_admin_login)
        self.assertTemplateUsed('jellyglass/wordpress.html')

        spoon = Spoon.objects.first()
        self.assertEqual(spoon.jelly, 'Wordpress')
        self.assertEqual(spoon.url, 'http://testserver' + path)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, extra['HTTP_REFERER'])
        self.assertEqual(spoon.user_agent, extra['HTTP_USER_AGENT'])
        self.assertJSONEqual(spoon.get, {
            'reauth': '1',
            'redirect_to': 'http://testserver' + self.url_wordpress_admin,
        })
        self.assertJSONEqual(spoon.post, data)

    def test_login_post_no_data(self):
        response = self.client.post(self.url_wordpress_admin_login)
        self.assertContains(response, self.url_wordpress_admin)
        self.assertContains(response, self.url_wordpress_admin_login)
        self.assertTemplateUsed('jellyglass/wordpress.html')

        spoon = Spoon.objects.first()
        self.assertEqual(spoon.jelly, 'Wordpress')
        self.assertEqual(spoon.url, 'http://testserver' + self.url_wordpress_admin_login)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, 'N/A')
        self.assertEqual(spoon.user_agent, 'N/A')
        self.assertJSONEqual(spoon.get, {'reauth': '', 'redirect_to': ''})
        self.assertJSONEqual(spoon.post, {
            'log': '',
            'pwd': '',
            'redirect_to': '',
            'rememberme': '',
            'testcookie': '',
            'wp-submit': ''
        })

    def test_login_post_ignore_unused(self):
        path = self.url_wordpress_admin_login + '?other=value'
        data = {
            'invalid': 'data',
        }
        response = self.client.post(path, data=data)
        self.assertContains(response, self.url_wordpress_admin)
        self.assertContains(response, self.url_wordpress_admin_login)
        self.assertTemplateUsed('jellyglass/wordpress.html')

        spoon = Spoon.objects.first()
        self.assertEqual(spoon.jelly, 'Wordpress')
        self.assertEqual(spoon.url, 'http://testserver' + path)
        self.assertEqual(spoon.remote_addr, '127.0.0.1')
        self.assertEqual(spoon.referer, 'N/A')
        self.assertEqual(spoon.user_agent, 'N/A')
        self.assertJSONEqual(spoon.get, {'reauth': '', 'redirect_to': ''})
        self.assertJSONEqual(spoon.post, {
            'log': '',
            'pwd': '',
            'redirect_to': '',
            'rememberme': '',
            'testcookie': '',
            'wp-submit': ''
        })
