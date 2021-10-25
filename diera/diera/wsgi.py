"""
WSGI config for diera project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diera.settings')

# Load the .env file
project_folder = os.path.expanduser('~/Projects/diera-prod/diera')
load_dotenv(dotenv_path="/home/marcus/Projects/diera-prod/diera/.env")

application = get_wsgi_application()
