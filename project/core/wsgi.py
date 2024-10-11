import os
from dj_static import Cling
from django.core.wsgi import get_wsgi_application
from core.settings.utils import get_settings_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", get_settings_module())

application = Cling(get_wsgi_application())
