from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from django.core.mail import send_mail
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagnostic.settings')
app = Celery('app1',backend=settings.CELERY_RESULT_BACKEND,broker=settings.CELERY_BROKER_URL)
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object(settings, namespace='CELERY')
# app.conf['CELERY_IMPORTS'] = settings.CELERY_IMPORTS
# print(app.conf.beat_schedule)
# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail': {
        'task': 'diagnostic.celery.send_mail_func',
        'schedule': crontab(minute='*/1'),
        # 'args': ('Firstdata',)
    }
}
# print(app.conf.beat_schedule)
# app.conf.beat_schedule = {  
#     'send-every-friday': {  
#         'task': 'app1.task.send_mail_func',  
#         'schedule': crontab(hour=7, minute=30, day_of_week=5),  
#         'args': ('Its Friday!',)  
#     },  
# }
# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
# @app.task(bind=True)
# # @shared_task(bind=True)
# def send_mail_func(self):
#     print("----------------")
#     send_mail(str("Payment Remainder | Dignostica Span" ),
#               "Celery Testing",
#               settings.EMAIL_HOST_USER,
#               ["sandeep.nexevo@gmail.com"],
#               fail_silently=False
#               )
#     # bookings=Prescriptionbook1.objects.filter(payment_status=False)
#     # for booking in bookings:
#     #     if (booking.test_name.first()!=True) and (bool(booking.prescription_file)==True and bool(booking.report) == False) and booking.payment_status==False: 
#     #         # print("sent")
#     #         # link=request.build_absolute_uri('/bookinghistory/')
#     #         send_mail(str("Payment Remainder | Dignostica Span" ),
#     #                     (f"Hi {booking.user.first_name} ,\nThis mail is regarding the booking id: {booking.bookingid}, recently booked by you, \nWe have reviewed your prescription and have added the tests for your testing Please check your dashboard,\nKindly visit your dashboard to review it and pay the mentioned amount to confirm the booking.\nHave a speedy and healthy recovery.\nThank you,\nDignostica Span"),
#     #                     settings.EMAIL_HOST_USER,
#     #                     [booking.user.email],
#     #                     fail_silently=False)
#     return "Done"