import os
import sys

sys.path.append('/srv/www/caseinsensitive.org/')

os.environ['PYTHON_EGG_CACHE'] = '/srv/www/caseinsensitive.org/.python-egg'
os.environ['DJANGO_SETTINGS_MODULE'] = 'casei.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
