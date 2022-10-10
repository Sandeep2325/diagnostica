# from django.contrib.auth import get_user_model
from celery import shared_task
from django.core.mail import send_mail
# from diagnostic.celery import app
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
# app.autodiscover_tasks()
# @app.task

@shared_task()
def send_mail_func():
    print("----------------")
    # send_mail(str("Payment Remainder | Diagnostica Span" ),
    #           "Celery Testing",
    #           settings.EMAIL_HOST_USER,
    #           ["sandeep.nexevo@gmail.com"],
    #           fail_silently=False
    #           )
    bookings=Prescriptionbook1.objects.filter(payment_status=False)
    for booking in bookings:
        # print(booking.test_name.first()!,bool(booking.test_name.first()!))
        if (booking.test_name.first()!=True) and (bool(booking.prescription_file)==True and bool(booking.report) == False) and booking.payment_status==False: 
            # print("sent")
            # link=request.build_absolute_uri('/bookinghistory/')
            send_mail(str(f"Payment Remainder | Booking Id:{booking.bookingid} | Diagnostica Span" ),
                        (f"Hi {booking.user.first_name} ,\nThis mail is regarding the booking id: {booking.bookingid}, recently booked by you, \nWe have reviewed your prescription and have added the tests for your testing Please check your dashboard,\nKindly visit your dashboard to review it and pay the mentioned amount to confirm the booking.\nHave a speedy and healthy recovery.\nThank you,\nDignostica Span"),
                        settings.EMAIL_HOST_USER,
                        [booking.user.email],
                        fail_silently=False)
    return "Done"

# @app.task
@shared_task()
def reportsavee():
    # print("-------------fgdgd")
    precbook=Prescriptionbook1.objects.filter(report="")
    tesbook=testbook.objects.filter(report="",payment_status=True)
    # print(precbook,tesbook)
    for book in precbook:
        # print("-------------insideloop")
        try:
            cre=creliohealthdata.objects.filter(spanbookingid=book.bookingid)
            for i in cre:
                # print("-------------")
                # token=""
                # billid=""
                if (bool(book.report) == False) and i.notify==False:
                    url = f"https://livehealth.solutions/getOrderStausPDFWithAllReports/?token={i.labtoken}&billId={i.billid}&isHeaderFooter=0"
                    payload={}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    # print(response.text)
                    resp=json.loads(response.text)
                    # print("-----------",resp)
                    if resp["code"]==200:
                        # print("send mail")
                        # print(resp["allReportDetails"]["reportDetails"])
                        a=resp["allReportDetails"]["reportDetails"]
                        datas = ContentFile(base64.b64decode(a), name=f'Report-{book.bookingid}.' + "pdf")
                        b=Prescriptionbook1.objects.filter(bookingid=book.bookingid)
                        for j in b:
                            j.report=File(datas)
                            j.save()
                        send_mail(str(f"Report | Booking Id:{book.bookingid} | Diagnostica Span" ),
                            f"Hello {b.user.first_name}\nYour Report is uploaded to your Dashboard for Booking Id:{book.bookingid}\nPlease Verify\nThank you \nDiagnostica Span",
                            settings.EMAIL_HOST_USER,
                            ["sandeep.nexevo@gmail.com"],
                            fail_silently=False
                            )
                        cre.update(notify=True)
        except Exception as e:
            print(e)
            pass
    for book in tesbook:
        # print("-------------insideloop1")
        try:
            cre=creliohealthdata.objects.filter(spanbookingid=book.bookingid)
            for i in cre:
                # print("-------------")
                # token=""
                # billid=""
                if (bool(book.report) == False) and i.notify==False:
                    url = f"https://livehealth.solutions/getOrderStausPDFWithAllReports/?token={i.labtoken}&billId={i.billid}&isHeaderFooter=0"
                    payload={}
                    headers = {}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    # print(response.text)
                    resp=json.loads(response.text)
                    # print("-----------",resp)
                    if resp["code"]==200:
                        # print("send mail")
                        # print(resp["allReportDetails"]["reportDetails"])
                        a=resp["allReportDetails"]["reportDetails"]
                        datas = ContentFile(base64.b64decode(a), name=f'Report-{book.bookingid}.' + "pdf")
                        b=testbook.objects.filter(bookingid=book.bookingid)
                        for j in b:
                            j.report=File(datas)
                            j.save()
                        send_mail(str(f"Report | Booking Id:{book.bookingid} | Diagnostica Span" ),
                           f"Hello {b.user.first_name}\nYour Report is uploaded to your Dashboard for Booking Id:{book.bookingid}\nPlease Verify\nThank you \nDiagnostica Span",
                           settings.EMAIL_HOST_USER,
                           ["sandeep.nexevo@gmail.com"],
                           fail_silently=False
                           )
                        cre.update(notify=True)
        except Exception as e:
            print(e)
            pass
    # return "Saved"
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


