import json

from django.contrib import admin
from django.utils.html import format_html, format_html_join

from .models import Spoon


class SpoonAdmin(admin.ModelAdmin):

    list_display = ['jelly', 'accessed', 'remote_addr', 'url']
    list_filter = ['jelly', 'accessed', 'remote_addr']

    def get_fields(self, request, obj=None):
        return [
            f.name for f in obj._meta.get_fields()
            if (f.name not in {'get', 'post'})
        ] + [
            'get_pretty', 'post_pretty'
        ]

    def get_readonly_fields(self, request, obj=None):
        return self.get_fields(request, obj)

    def _json_as_dl(self, j):
        data = json.loads(j)
        items = format_html_join(
            '',
            '<dt>{}</dt><dd>{}</dd>',
            (item for item in sorted(data.items()))
        )

        return format_html('<dl style="margin-left: 170px">{}</dl>', items)

    def get_pretty(self, obj):
        return self._json_as_dl(obj.get)
    get_pretty.short_description = 'GET'

    def post_pretty(self, obj):
        return self._json_as_dl(obj.post)
    post_pretty.short_description = 'POST'

admin.site.register(Spoon, SpoonAdmin)
