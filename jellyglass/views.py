from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render

from .utils import record_spoon


def django_admin(request):
    to = reverse('jellyglass:django_admin_login') + '?next=' + reverse('jellyglass:django_admin')
    return redirect(to)


@record_spoon('django')
def django_admin_login(request):
    return render(request, 'jellyglass/django.html')
