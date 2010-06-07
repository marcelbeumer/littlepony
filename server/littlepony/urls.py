from django.conf.urls.defaults import *
from littlepony.util.urlexamples import *
from django.conf import settings
import os

# standard littlepony index page
urlpatterns = patterns('littlepony.util.views',
    url(r'^$', 'index'),
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
    })
)

# YOUR url examples. Will be used to generate static exports and render the index.
# Just a few examples below based on the example urlpatterns
urlexamples = (
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
    urlexample('/test/sample/', description="Test page for json databinding"),
)