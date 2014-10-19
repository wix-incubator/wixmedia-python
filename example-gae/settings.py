# -*- coding: utf-8 -*- #

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': '',                      # Or path to database file if using sqlite3.
#         'USER': '',                      # Not used with sqlite3.
#         'PASSWORD': '',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }

TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False


LANGUAGES = (
    ('en', u'English'),
    # ('he', u'Hebrew'),
    # ('ru', u'Russian'),
)

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False


TEMPLATE_DIRS = (
    'templates',
)

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )

INSTALLED_APPS = (
    'media-django',
)

SECRET_KEY = 'SECRET_KEY'

WIXMEDIA_ROOT = 'http://endpoint.com'


