# Django settings for server project.
import os, sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
VIEWDATA_PATH = os.path.join(ROOT_PATH, 'viewdata')
STATIC_EXPORT_PATH = os.path.join(ROOT_PATH, "staticexports")

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = 'b3wknn$rdncvghzn5=nxwnnm%v9o@&=$i43=9q@pt!87fods9v'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'littlepony.middleware.ValidateHTML5',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'littlepony',
)

EXPORTURLEXAMPLES_INDEX_TEMPLATE = "builtin/staticexport_index.html"
