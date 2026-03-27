import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()

def handler(request, context=None):
    return app(request, context)
