from django.db import models
from django.utils.timezone import now

from .utils import dump_fields, filter_sensitive_data


class Spoon(models.Model):
    jelly = models.CharField(max_length=50)
    accessed = models.DateTimeField()

    url = models.URLField('URL')
    remote_addr = models.GenericIPAddressField('Remote address', null=True)
    referer = models.TextField('Referer')
    user_agent = models.TextField('User agent')

    get = models.TextField('GET')
    post = models.TextField('POST')

    def save(self, *args, **kwargs):
        self.accessed = now()
        super(Spoon, self).save(*args, **kwargs)

    @classmethod
    def from_request(cls, request, jelly, get_fields=None, post_fields=None):
        get_fields = get_fields or []
        post_fields = post_fields or []
        spoon = cls(jelly=jelly)

        spoon.url = request.build_absolute_uri()
        spoon.remote_addr = request.META.get('REMOTE_ADDR')
        spoon.referer = request.META.get('HTTP_REFERER', 'N/A')
        spoon.user_agent = request.META.get('HTTP_USER_AGENT', 'N/A')

        spoon.get = dump_fields(request.GET.dict(), get_fields)

        filtered_data = filter_sensitive_data(request, request.POST.dict())
        spoon.post = dump_fields(filtered_data, post_fields)

        spoon.save()
        return spoon
