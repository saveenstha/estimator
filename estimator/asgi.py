
import os
import environ
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estimator.settings')

application = get_asgi_application()
