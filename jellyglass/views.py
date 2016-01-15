import functools

from django.contrib.staticfiles.views import serve
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt

from .utils import record_spoon


def django_admin(request):
    to = reverse('jellyglass:django_admin_login') + '?next=' + reverse('jellyglass:django_admin')
    return redirect(to)


@record_spoon('Django',
              get_fields=['next'],
              post_fields=['username', 'password', 'next'],
              sensitive=['password'])
def django_admin_login(request):
    return render(request, 'jellyglass/django.html')


def wordpress_admin(request):
    path = reverse('jellyglass:wordpress_admin_login')
    to = '{scheme}://{host}{path}?redirect_to={current_uri}&reauth=1'.format(
        scheme=request.scheme, host=request.get_host(),
        path=path, current_uri=urlquote(request.build_absolute_uri(), safe=None),
    )
    return redirect(to)


@csrf_exempt
@record_spoon('Wordpress',
              get_fields=['redirect_to', 'reauth'],
              post_fields=['log', 'pwd', 'rememberme', 'wp-submit', 'redirect_to', 'testcookie'],
              sensitive=['pwd'])
def wordpress_admin_login(request):
    context = {
        'domain': '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host()),
    }
    return render(request, 'jellyglass/wordpress.html', context)


static = functools.partial(serve, insecure=True)
