import functools
import json

from django.conf import settings
from django.views.debug import CLEANSED_SUBSTITUTE
from django.views.decorators.debug import sensitive_post_parameters


def dump_fields(data, fields):
    if fields == "__ALL__":
        return json.dumps(data)
    else:
        return json.dumps({k: data.get(k, '') for k in fields})


def filter_sensitive_data(request, data):
    sensitive_post_parameters = getattr(request, 'sensitive_post_parameters', [])
    if (
        sensitive_post_parameters and
        getattr(settings, 'JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS', False)
    ):
        new_data = data.copy()
        if sensitive_post_parameters == '__ALL__':
            # Cleanse all parameters.
            for k, v in new_data.items():
                new_data[k] = CLEANSED_SUBSTITUTE
        else:
            # Cleanse only the specified parameters.
            for param in sensitive_post_parameters:
                if param in new_data:
                    new_data[param] = CLEANSED_SUBSTITUTE
        return new_data
    else:
        return data


def record_spoon(jelly, get_fields=None, post_fields=None, sensitive=None):
    from .models import Spoon

    def decorator(wrapper):
        @functools.wraps(wrapper)
        def view(request):
            if request.method == "POST":
                Spoon.from_request(request, jelly, get_fields, post_fields)
            return wrapper(request)

        if sensitive is not None and getattr(settings, 'JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS', False):
            view = sensitive_post_parameters(*sensitive)(view)
        return view
    return decorator
