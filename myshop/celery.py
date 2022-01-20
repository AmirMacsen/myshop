import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop', broker="amqp://guest:guest@192.168.33.136:5672/",
             backend="amqp://guest:guest@192.168.33.135:5672/")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)