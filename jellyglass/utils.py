from .models import Spoon


def record_spoon(jelly, get_fields=None, post_fields=None):
    def wrapper(f):
        def view(request):
            if request.method == "POST":
                Spoon.from_request(request, jelly, get_fields, post_fields)
            return f(request)
        return view
    return wrapper
