from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
# from app1.tasks import send_mail_func
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostic.settings')
app = Celery('diagnostic',broker_url='redis://127.0.0.1:6379/0')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail': {
        'task': 'app1.tasks.send_mail_func',
        # 'schedule': crontab(hour=0, minute=46, day_of_month=19, month_of_year = 6),
        'schedule': crontab(minute='*/1'),
        #'args': (2,)
    }
}
# app.conf.beat_schedule = {  
#     'send-every-friday': {  
#         'task': 'app1.tasks.send_mail_func',  
#         'schedule': crontab(hour=7, minute=30, day_of_week=5),  
#         'args': ('Its Friday!',)  
#     },  
# }
# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks()
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')