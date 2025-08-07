import os
import environ
from django.core.wsgi import get_wsgi_application

env = environ.Env()
environ.Env.read_env()
environment = env('ENVIRONMENT', default='prod')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'estimator.settings.{environment}')

application = get_wsgi_application()
