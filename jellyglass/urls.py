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

    return patterns

urlpatterns = get_urls()
