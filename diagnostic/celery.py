from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# from app1.tasks import send_mail_func
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostic.settings')
app = Celery('app1',backend=settings.CELERY_RESULT_BACKEND,broker=settings.CELERY_BROKER_URL)
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
# app.conf.beat_schedule = {
#     'send-mail': {
#         'task': 'app1.task.send_mail_func',
       
#         'schedule': crontab(minute='*/1'),
#     }
# }
# app.conf.beat_schedule = {  
#     'send-every-friday': {  
#         'task': 'app1.task.send_mail_func',  
#         'schedule': crontab(hour=7, minute=30, day_of_week=5),  
#         'args': ('Its Friday!',)  
#     },  
# }
# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')