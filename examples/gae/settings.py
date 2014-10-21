# -*- coding: utf-8 -*- #

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

INSTALLED_APPS = (
)

SECRET_KEY = 'SECRET_KEY'


