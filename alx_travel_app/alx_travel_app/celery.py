# celery.py file for setting up Celery in a Django project
# alx_travel_app/alx_travel_app/celery.py
# This file configures Celery to work with the Django project.
# It sets the default Django settings module for the 'celery' program.
# It also creates a Celery application instance and auto-discovers tasks from all registered Django app configs.
# It is important to ensure that this file is correctly set up for Celery to function properly in the Django environment.

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

app = Celery('alx_travel_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# ==> this is done to ensure the app is always imported when
# Django starts so that shared tasks use this app.