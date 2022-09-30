# from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
from diagnostic.celery import app
import requests
import json
import base64
from django.core.files.base import ContentFile
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

@app.task(bind=True)
def reportsavee(self):
    precbook=Prescriptionbook1.objects.filter(report__is_null=True)
    tesbook=testbook.objects.filter(report__is_null=True,payment_status=True)
    for book in precbook:
        try:
            cre=creliohealthdata.objects.filter(spanbookingid=book.bookingid)
            for i in cre:
                # token=""
                # billid=""
                if (bool(book.report) == False) and i.notify==False:
                    url = f"https://livehealth.solutions/getOrderStausPDFWithAllReports/?token={i.labtoken}&billId={i.billid}"
                    payload={}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    # print(response.text)
                    resp=json.loads(response.text)
                    if resp["code"]==200:
                        # print("send mail")
                        # print(resp["allReportDetails"]["reportDetails"])
                        a=resp["allReportDetails"]["reportDetails"]
                        datas = ContentFile(base64.b64decode(a), name=f'Report-{book.bookingid}.' + "pdf")
                        b=Prescriptionbook1.objects.filter(bookingid=book.bookingid)
                        for j in b:
                            j.report=File(datas)
                            j.save()
                        send_mail(str(f"Report|Booking Id:{book.bookingid} | Dignostica Span" ),
                            f"Hello {b.user.first_name}\nYour Report is uploaded to your Dashboard for Booking Id:{book.bookingid}\nPlease Verify\nThank you \nDiagnostica Span",
                            settings.EMAIL_HOST_USER,
                            ["sandeep.nexevo@gmail.com"],
                            fail_silently=False
                            )
                        cre.update(notify=True)
        except:
            pass
    for book in tesbook:
        try:
            cre=creliohealthdata.objects.filter(spanbookingid=book.bookingid)
            for i in cre:
                # token=""
                # billid=""
                if (bool(book.report) == False) and i.notify==False:
                    url = f"https://livehealth.solutions/getOrderStausPDFWithAllReports/?token={i.labtoken}&billId={i.billid}"
                    payload={}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    # print(response.text)
                    resp=json.loads(response.text)
                    if resp["code"]==200:
                        # print("send mail")
                        # print(resp["allReportDetails"]["reportDetails"])
                        a=resp["allReportDetails"]["reportDetails"]
                        datas = ContentFile(base64.b64decode(a), name=f'Report-{book.bookingid}.' + "pdf")
                        b=testbook.objects.filter(bookingid=book.bookingid)
                        for j in b:
                            j.report=File(datas)
                            j.save()
                        send_mail(str(f"Report|Booking Id:{book.bookingid} | Dignostica Span" ),
                           f"Hello {b.user.first_name}\nYour Report is uploaded to your Dashboard for Booking Id:{book.bookingid}\nPlease Verify\nThank you \nDiagnostica Span",
                           settings.EMAIL_HOST_USER,
                           ["sandeep.nexevo@gmail.com"],
                           fail_silently=False
                           )
                        cre.update(notify=True)
        except:
            pass
        # for i in precbook:
        #     if i.
# a={"code": 200,
#     "allReportDetails": {
#       "Gender": "Male",
#       "Age": "24 years",
#       "Contact No": "9405751941",
#       "Patient Name": "Jane Doe",
#       "billId": "17758",
#       "labPatientId": "Lab1234",
#       "reportDetails": "oooo",
#       "Patient Id": 20185
#     }
#     }
# print(a["code"])


