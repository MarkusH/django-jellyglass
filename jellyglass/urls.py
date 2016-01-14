from django.conf import settings
from django.conf.urls import url

from . import views


def get_urls():
    patterns = []

    if getattr(settings, 'JELLYGLASS_DJANGO', True):
        patterns.extend([
            url(r'^admin/$', views.django_admin, name='django_admin'),
            url(r'^admin/login/$', views.django_admin_login, name='django_admin_login'),
        ])

    if getattr(settings, 'JELLYGLASS_WORDPRESS', True):
        patterns.extend([
            url(r'^wp-admin/$', views.wordpress_admin, name='wordpress_admin'),
            url(r'^wp-admin.php$', views.wordpress_admin_login, name='wordpress_admin_login'),
            url(r'^wp-includes/css/buttons.min.css$', views.static, {'path': 'css/wordpress/buttons.min.css'}),
            url(r'^wp-includes/css/dashicons.min.css$', views.static, {'path': 'css/wordpress/dashicons.min.css'}),
            url(r'^wp-admin/css/login.min.css$', views.static, {'path': 'css/wordpress/login.min.css'}),
            url(r'^wp-admin/images/wordpress-logo.svg$', views.static, {'path': 'img/wordpress/wordpress-logo.svg'}),
        ])

    return patterns

urlpatterns = get_urls()
