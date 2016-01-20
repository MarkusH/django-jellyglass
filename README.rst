=================
django-jellyglass
=================

.. image:: https://img.shields.io/pypi/v/django-jellyglass.svg
   :target: https://pypi.python.org/pypi/django-jellyglass

.. image:: https://img.shields.io/pypi/l/django-jellyglass.svg
   :target: https://pypi.python.org/pypi/django-jellyglass

.. image:: https://img.shields.io/travis/MarkusH/django-jellyglass.svg
   :target: https://travis-ci.org/MarkusH/django-jellyglass


**django-jellyglass** is a reusable Django application to act as a better
honeypot.


Installation
============

Use PIP to install **django-jellyglass** from PyPI::

   $ pip install django-jellyglass

Add ``jellyglass.apps.JellyGlassConfig`` to your ``INSTALLED_APPS``::

   INSTALLED_APPS = [
       # ...
       'jellyglass.apps.JellyGlassConfig',
   ]

Add the following ``urlpatterns`` to your root url configuration::

   urlpatterns = [
       # ...
       url(r'^', include('jellyglass.urls', namespace='jellyglass')),
       # ...
   ]

Run migrations::

   $ python manage.py migrate
   Operations to perform:
     Apply all migrations: admin, auth, contenttypes, jellyglass, sessions
   Running migrations:
     Rendering model states... DONE
     Applying jellyglass.0001_initial... OK


Settings
========

Enable or disable the Django admin with::

   JELLYGLASS_DJANGO = True

Enable or disable the Wordpress admin with::

   JELLYGLASS_WORDPRESS = True

Enable or disable the recording of sensitive data with::

   JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS = False

In case you're behind a reverse proxy (e.g. Apache, Nginx) this setting can be
used to specify where the actual ``REMOTE_ADDR`` is stored::

   JELLYGLASS_HIDE_SENSITIVE_POST_PARAMETERS = 'REMOTE_ADDR'
   # For a header 'X-REAL-IP' this would be 'HTTP_X_REAL_IP'
