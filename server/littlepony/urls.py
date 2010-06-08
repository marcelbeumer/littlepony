from django.conf.urls.defaults import *
from littlepony.util.urlexamples import *
from django.conf import settings
import os

# standard littlepony index page
urlpatterns = patterns('littlepony.util.views',
    url(r'^$', 'index', name="littlepony_index"),
    url(r'^manual/$', 'manual', name="littlepony_manual"),
)

# YOUR views, just a few examples below
urlpatterns += patterns('littlepony.views',
    url(r'^products/$', 'products', name="products"),
    url(r'^(?P<template>[a-z\-_]+)/(?P<jsonfile>[a-z\-_]+)/$', 'json_page', name="json_page"),
    url(r'^(?P<template>[a-z\-_]+)/$', 'page', name="page"),
)

# setup to serve static files
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.ROOT_PATH, 'media'),
    }),
    url(r'^docs/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.ROOT_PATH, 'docs'),
    }),
)

# YOUR url examples. Will be used to generate static exports and render the index.
# Just a few examples below based on the example urlpatterns
urlexamples = (
    urlexample('/manual/', description="Little pony manual", noexport=True),
    urlexample('/docs/django_docs-1.2/index.html', description="Official Django 1.2 documentation", noexport=True),
    urlexample('/docs/python-2.6.2-docs/index.html', description="Official Python 2.6 documentation", noexport=True),
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
)