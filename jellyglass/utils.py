from .models import Spoon


def record_spoon(jelly):
    def wrapper(f):
        def view(request):
            if request.method == "POST":
                Spoon.from_request(jelly, request)
            return f(request)
        return view
    return wrapper
