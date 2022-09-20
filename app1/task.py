# from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from diagnostic.celery import app
# from diagnostic import settings
# from django.utils import timezone
# from datetime import timedelta
from .models import *
from django.conf import settings
from time import sleep
# @shared_task(bind=True)
app.autodiscover_tasks()
@app.task(bind=True)
def send_mail_func(self):
    print("----------------")
    send_mail(str("Payment Remainder | Dignostica Span" ),
              "Celery Testing",
              settings.EMAIL_HOST_USER,
              ["sandeep.nexevo@gmail.com"],
              fail_silently=False
              )
    # bookings=Prescriptionbook1.objects.filter(payment_status=False)
    # for booking in bookings:
    #     if (booking.test_name.first()!=True) and (bool(booking.prescription_file)==True and bool(booking.report) == False) and booking.payment_status==False: 
    #         # print("sent")
    #         # link=request.build_absolute_uri('/bookinghistory/')
    #         send_mail(str("Payment Remainder | Dignostica Span" ),
    #                     (f"Hi {booking.user.first_name} ,\nThis mail is regarding the booking id: {booking.bookingid}, recently booked by you, \nWe have reviewed your prescription and have added the tests for your testing Please check your dashboard,\nKindly visit your dashboard to review it and pay the mentioned amount to confirm the booking.\nHave a speedy and healthy recovery.\nThank you,\nDignostica Span"),
    #                     settings.EMAIL_HOST_USER,
    #                     [booking.user.email],
    #                     fail_silently=False)
    return "Done"

