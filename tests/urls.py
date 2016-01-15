from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('jellyglass.urls', namespace='jellyglass')),
    url(r'^real-admin/', admin.site.urls),
]
