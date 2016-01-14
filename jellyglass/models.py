import json

from django.db import models
from django.utils.timezone import now


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
    def from_request(cls, jelly, request):
        spoon = cls(jelly=jelly)

        spoon.url = request.build_absolute_uri()
        spoon.remote_addr = request.META.get('REMOTE_ADDR')
        spoon.referer = request.META.get('HTTP_REFERER', 'N/A')
        spoon.user_agent = request.META.get('HTTP_USER_AGENT', 'N/A')

        spoon.get = json.dumps(request.GET.dict())
        spoon.post = json.dumps(request.POST.dict())

        spoon.save()
