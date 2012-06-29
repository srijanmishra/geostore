# Django settings for orbitnote project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Vibhaj Rajan', 'vibhaj8@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'geostore',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'krishna',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/ui/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	'C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/geostore/ui',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u0&amp;1650h@d-7t^$kub9vks8swg$0#a=kc9sno-5=c_y0p!&amp;k*-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'geostore.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'geostore.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../tpl').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
	# 'django_openid_auth',	# OpenID Authentication
	'kestrel.graph',
	'kestrel.people',
	'kestrel.storage'
)

AUTHENTICATION_BACKENDS = (
	#'django_openid_auth.auth.OpenIDBackend',
	'django.contrib.auth.backends.ModelBackend',
	#'kestrel.auth.glopenid.GoogleBackend',
)

AUTH_PROFILE_MODULE = 'people.Person'

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

# OpenID Authentication
OPENID_CREATE_USERS = True
OPENID_UPDATE_DETAILS_FROM_SREG = True
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'
OPENID_SSO_SERVER_URL = 'https://www.google.com/accounts/o8/id'

# geostore settings
ROOTPATH = 'http://127.0.0.1:8080'

# kestrel  people settings
PEOPLE_ID = 0
PEOPLE_VERIFY_EXPIRY = 5
PEOPLE_VERIFY_SUBJECT = 'GeoStore Account Verification'
PEOPLE_VERIFY_BODY = 'Hello %(username)s,\nYour GeoStore account was created successfully.\n\nPlease click on the following link to verify your registration:\n'+ ROOTPATH +'/verify/%(username)s/%(verify)s/\n\nRegards,\nTeam GeoStore\n'
PEOPLE_RESET_SUBJECT = 'GeoStore Password Reset'
PEOPLE_RESET_BODY = 'Hello %(username)s,\nYour GeoStore password was reset successfully.\n\nPlease use the following password to access your account:\n\nUsername : %(username)s\nPassword : %(password)s\n\nRegards,\nTeam GeoStore\n'

# kestrel  storage settings
STORAGE_ID = 0
STORAGE_PRIVATE_ROOT = 'C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/geostore/storage'
STORAGE_PUBLIC_ROOT = 'C:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/geostore/ui/files'

# email settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'support@orbitnote.com'
EMAIL_HOST_PASSWORD = 'Orb17N0t3'
EMAIL_USE_TLS = True

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
