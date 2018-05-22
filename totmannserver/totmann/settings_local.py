# Configure your local django settings here.
# Please consult https://docs.djangoproject.com/en/1.8/ref/settings/
# for a list of settings and their meanings.
#
# Rename this file to settings_local.py inside the totmann subdirectory.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Configure the path and URL for static files
#STATIC_ROOT = os.path.join(BASE_DIR, "public")
#STATIC_URL = '/'

# Add your hostname here
ALLOWED_HOSTS = ['*']

# For testing, enable debugging (but never in production!)
DEBUG = False
# TEMPLATE_DEBUG = True

# Configure a database here (omit if you want to use sqlite as configured in settings.py)
# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'totmann',
#        'USER': 'totmann',
#        'PASSWORD': "totmann",
#        'HOST': 'localhost',
#    }
# }

#SECRET_KEY = '--some random string here, e.g., 64 random characters--'

# Needed only if run behind a proxy.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_SSL', 'on')

# Configure email backend.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'totmann-smtp-server.example'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'totmann'
EMAIL_HOST_PASSWORD = 'totmannsecret'
EMAIL_USE_TLS = True
