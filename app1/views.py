import itertools
import re
import os
# import sweetify
from django.shortcuts import render,redirect
from .forms import UserProfileForm,UserRegistrationForm, forgotpasswordform, subscriptionform
from django.contrib.auth.hashers import make_password
import random
from app1.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import uuid
import json
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import FileResponse
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.views import View
import razorpay
from django.contrib.auth import logout
from django.db.models import Q
from django.conf import settings
import environ
import shortuuid
from num2words import num2words
import re
from datetime import datetime,timezone 
from django.core import serializers
import threading
import time
# from threading import Thread
env = environ.Env()
global OBJ_COUNT
OBJ_COUNT = 0
checkk=[]
teest=[]
packagee=[]
Bangalore=env("Bangalore")
Mumbai=env("Mumbai")
Bhophal=env("Bhophal")
Nanded=env("Nanded")
Pune=env("Pune")
Barshi=env("Barshi")
Aurangabad=env("Aurangabad")
shipping_charges=199
# reachus=["reachus@spanhealth.com"]
reachus=["sandeep.nexevo@gmail.com"]
gosamplify_apikey="8517db-ff9614-42c7c9-512743-18780d" 
customer_code="DIS"     
class customerEmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.emailfrom=settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        # self.html_content = html_content
        threading.Thread.__init__(self)
    def run (self):
        try:
            send_mail(
                    self.subject,
                    self.message,
                    self.emailfrom,
                    self.recipient_list,
                    fail_silently=False,
                    )
        except:
            pass
class AdminEmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.emailfrom=settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        # self.html_content = html_content
        threading.Thread.__init__(self)
    def run (self):
        # print("----------",self.recipient_list)
        try:
            send_mail(
                    self.subject,
                    self.message,
                    self.emailfrom,
                    self.recipient_list,
                    fail_silently=False,
                    )
        except:
            pass
class countdownThread(threading.Thread):
    def __init__(self,timer,request):
        # print("---",timer)
        self.timer=timer
        self.request=request
        threading.Thread.__init__(self)
    def run (self):
        print("sel-------",self.timer)
        while self.timer:
            mins, secs = divmod(self.timer, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            minss='{:02d}'.format(mins)
            secss='{:02d}'.format(secs)
            a=self.request.session.get("otp")
            if minss=="00" and secss=="01":
                a=self.request.session.get("otp")
                if a!= None:
                    print(self.request)
                    del self.request.session['otp']
                    b=self.request.session.get("otp")
                    print("deleted",b)
            time.sleep(1)
            self.timer -= 1  
def indextable1(request):
    precriptionb = serializers.serialize("json", Prescriptionbook1.objects.all().order_by('-created')[0:10])
    return HttpResponse(precriptionb)
    # return HttpResponse(json.dumps(prescription_bookings),content_type="application/json")
def indextable2(request):
    precriptionb = serializers.serialize("json", testbook.objects.all().order_by('-created')[0:10])
    return HttpResponse(precriptionb)    
def dashboard(request):
    # test_bookings=prescription_book.objects.filter(test_name__isnull=True, prescription_file='').count()
    prescription_bookings=Prescriptionbook1.objects.all().count()
    testbooking=testbook.objects.all().count()
    packages=healthpackages.objects.all().count()
    bookamount=book_history.objects.all()
    outstand=book_history.objects.filter(payment_status=False)
    totalamount=[]
    outstandingamount=[]
    for i in bookamount:
        if i.amount is not None:
            totalamount.append(int(float(i.amount)))
    for i in outstand:
        if i.amount is not None:
            outstandingamount.append(int(float(i.amount)))
    # prescription_bookings1=test-test_bookings
    bookings=int(testbooking)+int(prescription_bookings)
    context={
        "test":bookings,
        "test_bookings":testbooking,
        "prescription_bookings":prescription_bookings,
        "packages":packages,
        "totalamount":'₹'+str(sum(totalamount)),
        "outstandingamount":'₹'+str(sum(outstandingamount))
    }
    return HttpResponse(json.dumps(context),content_type="application/json")

def aboutus(request):
    return render (request,"aboutus.html")
def cityy(request):
    city=request.POST.get("city")
    code=request.POST.get("code")
    request.session["city"]="Bangalore"
    request.session["tempcity"]=city
    request.session["citycode"]=code
    return JsonResponse({"message":True,"city":city})

def Registration(request):
    if request.method == "POST":
        fm = UserRegistrationForm(request.POST)
        up = UserProfileForm(request.POST)
        # if fm.is_valid():
        e = request.POST['email']
        f = request.POST['firstname']
        l = request.POST['lastname']
        p = request.POST['confirmpassword']
        p_number = request.POST['phone']
        user=User.objects.filter(email=e)
        if user.exists():
            messages.error(request,"Email is already registered")
            return render(request,'register.html')
        if User.objects.filter(phone_no=p_number).exists():
            messages.error(request,"Mobile Number Already Exists")
            return render(request,'register.html')
        else:
            request.session['email'] = e
            request.session['firstname'] = f
            request.session['lastname'] = l
            request.session['password'] = p
            request.session['number'] = p_number
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
            
                # f"Hi {f},\nThere was a request to change your password!\nIf you did not make this request then please ignore this email.\nOtherwise, please click this link to change your password: [link]"
            # message=f"Hi {f},\n\nGreetings!\nYou are just a step away from accessing your Diagnostica Span account.\nWe are sharing a verification code to access your account. Once you have verified the code, you'll be prompted to access our portal immediately.\n\nYour OTP: {otp}\n\nThank You,\nDiagnostica Span"
            # message = f'Welcome your otp is {otp} '
            message=f"{otp}- is your OTP for Spandiagno user registration. Please do not share this OTP with anyone. Spandiagno."
            message1=f"{otp}- is your one time password for Spandiagno user registration. Please do not share this OTP with anyone.\nThanks You\nDiagnostica Span."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            message = message
            subject = "DIAGNOSTICA SPAN OTP Confirmation" 
            a=sms(message,p_number)
            # countdown(int(10))
            # send_mail(
            #         subject,
            #         message1,
            #         email_from,
            #         recipient_list,
            #         fail_silently=False,
            # )
            # countdownThread(10,request).start()
            customerEmailThread(subject, message1, recipient_list).start()
            messages.info(request,a)
            return redirect('/registration/otp/')
    return render(request,'register.html')

def otpRegistration(request):
    if request.session.get("email") == None:
        return HttpResponseRedirect(reverse("Registration"))
    if request.method == "POST":
        u_otp1 = request.POST['digit-1']
        u_otp2 = request.POST['digit-2']
        u_otp3 = request.POST['digit-3']
        u_otp4 = request.POST['digit-4']
        a=str(u_otp1)+str(u_otp2)+str(u_otp3)+str(u_otp4)
        otp = request.session.get('otp')
        firstname = request.session['firstname']
        lastname = request.session['lastname']
        # hash_pwd=request.session.get('password')
        hash_pwd = make_password(request.session.get('password'))
        p_number = request.session.get('number')
        email_address = request.session.get('email') 
        try:
            if int(a) == otp:
                User.objects.create(
                                first_name = firstname,
                                last_name=lastname,
                                email=email_address,
                                phone_no=p_number,
                                password=hash_pwd
                )
                if request.session.get('otp')!=None:
                    del request.session['otp']
                if request.session.get('firstname')!=None:
                    del request.session['firstname']
                if request.session.get('lastname')!=None:
                    del request.session['lastname']
                if request.session.get('email')!=None:
                    del request.session['email']
                if request.session.get('password')!=None:
                    del request.session['password']
                if request.session.get('phone_number')!=None:
                    del request.session['phone_number']
                    # f"Hi {f},\nThere was a request to change your password!\nIf you did not make this request then please ignore this email.\nOtherwise, please click this link to change your password: [link]"
            # message=f"Hi {f},\n\nGreetings!\nYou are just a step away from accessing your Diagnostica Span account.\nWe are sharing a verification code to access your account. Once you have verified the code, you'll be prompted to access our portal immediately.\n\nYour OTP: {otp}\n\nThank You,\nDiagnostica Span"
            # message = f'Welcome your otp is {otp} '
                message=f"Hi {firstname} {lastname},Thank you for registering with us.\nYour one-stop solution for all diagnostic services.\nDiagnostica Span"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email_address]
                message = message
                subject = "DIAGNOSTICA SPAN OTP Confirmation" 
                a=sms(message,p_number)
                # send_mail(
                #         subject,
                #         message,
                #         email_from,
                #         recipient_list,
                #         fail_silently=False,
                # )
                customerEmailThread(subject, message, recipient_list).start()
                messages.success(request,'Registration Successfully Done !!')
                return redirect('/login/')
            else:
                messages.error(request,'Wrong OTP')
        except:
            messages.error(request,"Please Fill all Required Fields")
    return render(request,'otp.html')

def resendotp(request):
    # if request.method=="POST":
    email_address = request.session.get('email')
    p_number = request.session.get('number')
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    message=f"{otp}- is your OTP for Spandiagno for password to be resent. Please do not share this OTP with anyone. Spandiagno."
    message1=f"{otp}- is your OTP for Spandiagno for password to be resent. Please do not share this OTP with anyone.\nThank You\n Diagnostica Span."
    # message=f"Hi There,\nYou have requested a new One-Time-Password for verifying your account.\nKindly use the below OTP to proceed further steps.\nOTP: {otp}\nIf the request doesn't concern you, kindly ignore this mail.\nThank You,\nDIAGNOSTICA Span"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address]
    message = message
    subject = "OTP Verification | DIAGNOSTICA SPAN"
    try: 
        # userr=User.objects.get(email=email_address) 
        a=sms(message,p_number)
        # send_mail(
        #         subject,
        #         message1,
        #         email_from,
        #         recipient_list,
        #         fail_silently=False,
        # )
        customerEmailThread(subject, message1, recipient_list).start()
        messages.success(request,a)
    except:
        messages.warning(request,"Something went wrong")
    return redirect('/registration/otp/')
@login_required(login_url="/login/")
def changepassword(request):
    if request.method=="POST":
      password=request.POST["currentPassword"]
      conpassword=request.POST["confirmpassword"]
      otp = random.randint(1000,9999)
      email_address = request.user.email
      a=authenticate(request,username=request.user.email,password=password)
      if a == None:
          messages.info(request,"Invalid password")
          return render (request,"changepassword.html")
      else:
        request.session["ppassword"]=password 
        request.session["conpassword"]=conpassword
        request.session['otp'] = otp
        message=f"{otp}- is your OTP for Spandiagno to change password. Please do not share this OTP with anyone. Spandiagno."
        message1=f"{otp}- is your OTP for Spandiagno to change password. Please do not share this OTP with anyone.\nThanks You\nDiagnostica Span."
        # message=f"Hi {request.user.first_name},\nYou have requested to change your password credentials to login, please use below OTP to do the same\n\nOTP: {otp}\nIf the wish to keep your old password, kindly ignore the mail.\nThank you,\nDIAGNOSTICA Span"
        # message = f'Hello,\nWelcome your Change Password OTP is {otp} '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email_address]
        message = message
        subject = "DIAGNOSTICA SPAN" 
        p_number=request.user.phone_no
        a=sms(message,p_number)
        # send_mail(
        #         subject,
        #         message1,
        #         email_from,
        #         recipient_list,
        #         fail_silently=False,
        #     )
        customerEmailThread(subject, message1, recipient_list).start()
        messages.info(request,a)
        return redirect('/changepasswordotp/')
    return render (request,"changepassword.html")

def forgotpassword(request):
    if request.method=="POST":
        fm = forgotpasswordform(request.POST)
        e = request.POST['email']
            # u = fm.cleaned_data['password']
        p = request.POST['confirmpassword']
        user=User.objects.filter(email=e)
        
        if user.exists():
            userr=User.objects.get(email=e)
            request.session['email'] = e
            request.session['password'] = p
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
                # message = f'your otp is {otp}'
                # send_otp(p_number,message)
            message=f"{otp}- is your OTP for Spandiagno if you have forgotten password. Please do not share this OTP with anyone. Spandiagno. "
            message1=f"{otp}- is your OTP for Spandiagno if you have forgotten password. Please do not share this OTP with anyone\nThank You\nDiagnostica Span"
            # message = f"Hi Dear Customer,\nThere was a request to Forgot password! Password change\nIf you did not make this request then please ignore this email.\nOtherwise, Please enter the OTP {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            message = message
            subject = "DIAGNOSTICA SPAN | FORGOT PASSWORD"
            p_number=userr.phone_no
            # templateid=1507166152065523633
            a=sms(message,p_number)
            # send_mail(
            #         subject,
            #         message1,
            #         email_from,
            #         recipient_list,
            #         fail_silently=False,
            # )
            customerEmailThread(subject, message1, recipient_list).start()
            messages.info(request,a)
            return redirect('/forgotpassword/otp/')
        else:
            messages.error(request,"Email is not registered")
            return render(request,"forgotpassword.html")
    return render(request,"forgotpassword.html")
def resendotpforgot(request):
    # if request.method=="POST":
    email_address = request.session.get('email')
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    message=f"{otp}- is your OTP for Spandiagno for password to be resent. Please do not share this OTP with anyone. Spandiagno."
    message1=f"{otp}- is your OTP for Spandiagno for password to be resent. Please do not share this OTP with anyone.\nThank You\nDiagnostica Span"
    # message=f"Hi There,\nYou have requested a new One-Time-Password for verifying your account.\nKindly use the below OTP to proceed further steps.\nOTP: {otp}\nIf the request doesn't concern you, kindly ignore this mail.\nThank You,\nDIAGNOSTICA Span"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address]
    message = message
    subject = "OTP Verification | DIAGNOSTICA SPAN"
    try:
        userr=User.objects.get(email=email_address) 
        a=sms(message,userr.phone_no)
        # send_mail(
        #         subject,
        #         message1,
        #         email_from,
        #         recipient_list,
        #         fail_silently=False,
        # )
        customerEmailThread(subject, message1, recipient_list).start()
        messages.success(request,a)
    except:
        messages.warning(request,"Something went wrong")
    return redirect('forgotpassword/otp/')
def changeresend(request):
    # if request.method=="POST":
    email_address = request.session.get('email')
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    message=f"{otp}- is your OTP for Spandiagno for password to be resent. Please do not share this OTP with anyone. Spandiagno."
    message1=f"{otp}- is your OTP for Spandiagno for password to be resent. Please do not share this OTP with anyone.\nThank You\nDiagnostica Span."
    # message=f"Hi There,\nYou have requested a new One-Time-Password for verifying your account.\nKindly use the below OTP to proceed further steps.\nOTP: {otp}\nIf the request doesn't concern you, kindly ignore this mail.\nThank You,\nDIAGNOSTICA Span"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address]
    message = message
    subject = "OTP Verification | DIAGNOSTICA SPAN" 
    try:
        userr=User.objects.get(email=email_address) 
        a=sms(message,userr.phone_no)
        # send_mail(
        #         subject,
        #         message1,
        #         email_from,
        #         recipient_list,
        #         fail_silently=False,
        # )
        customerEmailThread(subject, message1, recipient_list).start()
        messages.success(request,a)
    except:
        messages.success(request,"Something went wrong")
    return redirect('changepasswordotp/')
def changepasswordotp(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("user-login"))
    if request.method == "POST":
        u_otp1 = request.POST['digit-1']
        u_otp2 = request.POST['digit-2']
        u_otp3 = request.POST['digit-3']
        u_otp4 = request.POST['digit-4']
        a=str(u_otp1)+str(u_otp2)+str(u_otp3)+str(u_otp4)
        otp = request.session.get('otp')
        # user = request.session['username']
        # hash_pwd=request.session.get('password')
        # hash_pwd = make_password(request.session.get('password'))
        # p_number = request.session.get('number')
        email_address = request.session.get('email') 
        password=request.session.get("ppassword")
        # request.session.get("newpassword")
        newpassword=make_password(request.session.get("conpassword"))
        try:
            if int(a) == otp:
                data = User.objects.filter(
                                email=request.user.email)
                if data.exists():
                    data.update(password=newpassword)
                # user_instance = User.objects.get(username=user)
                # User.objects.create(
                #                 user = user_instance,phone_number=p_number
                # )
                    request.session.delete("ppassword")
                # request.session.delete("newpassword")
                    request.session.delete("conpassword")
                    messages.success(request,'Password changed successfully!! Please Login Again.')
                    return redirect('user-login')
                else:
                    print("not exists")
            else:
                messages.error(request,'Wrong OTP')
        except:
            messages.error(request,"Please Fill all Required Fields")
    return render(request,'otpchange.html')    
def passwordcheck(request):
    if request.method=="POST":
        password=request.POST.get("password")
        try:
            a=authenticate(request,username=request.user.email,password=password)
            if a == None:
            # User.objects.get(email=request.user.email,password=password) 
                return JsonResponse({"message":False})
            else:
                return JsonResponse({"message":True})
        except Exception as e:
            return JsonResponse({"message":False})
def otpforgotpassword(request):
    if request.session.get("email") == None:
        return HttpResponseRedirect(reverse("Registration"))
    if request.method == "POST":
        u_otp1 = request.POST['digit-1']
        u_otp2 = request.POST['digit-2']
        u_otp3 = request.POST['digit-3']
        u_otp4 = request.POST['digit-4']
        a=str(u_otp1)+str(u_otp2)+str(u_otp3)+str(u_otp4)
        otp = request.session.get('otp')
        # user = request.session['username']
        # hash_pwd=request.session.get('password')
        hash_pwd = make_password(request.session.get('password'))
        # p_number = request.session.get('number')
        email_address = request.session.get('email') 
        try:
            if int(a) == otp:
                User.objects.filter(
                                email=email_address
                ).update(password=hash_pwd)
                request.session.delete('otp')
                request.session.delete('email')
                request.session.delete('password')
                messages.success(request,"Password Changed")
                return redirect('user-login')
            else:
                messages.error(request,'Wrong OTP')
        except:
            messages.error(request,"Please Fill all Required Fields")
    return render(request,'otpforgot.html') 
def forgotresendotp(request):
    # if request.method=="POST":
    email_address = request.session.get('email')
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    message=f"Hello,\nYour Rsend OTP is {otp}\nPlease enter to verify"
    # message=f"Hi Dear Customer,\nThere was a request to Forgot password! password change\nIf you did not make this request then please ignore this email.\nOtherwise, please enter the otp {otp}"
    # message = f'Welcome your resend otp is {otp} '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address]
    message = message
    subject = "OTP" 
    # send_mail(
    #         subject,
    #         message,
    #         email_from,
    #         recipient_list,
    #         fail_silently=False,
    # )
    messages.success(request,"resend otp sent")
    return redirect('/forgotpassword/otp/') 
def userinfo(request):
   a= request.user
   return JsonResponse({"message":True,"firstname":a.first_name,"lastname":a.last_name,"contact":a.phone_no,"gender":a.gender,"address":a.address,"age":a.age,"email":a.email}) 
@login_required(login_url="/login/")
def profilee(request):
    import datetime
    cityy=city.objects.filter(active=True)
    profile=User.objects.get(email=request.user.email)
    # dobstrp = datetime.datetime.strptime(profile.dob, '%y-%m-%d')
    # print("-----",dobstrp)
    if request.method=="GET":
        context={
            "profile":profile,
            "cityy":cityy,
        }
        return render (request,"profile.html",context)
    if request.method=="POST":
        profilepic=request.FILES.get("profile_pic", request.user.photo)
        firstname=request.POST.get("firstname",request.user.first_name)
        lastname=request.POST.get("lastname",request.user.last_name)
        email=request.POST.get("email",request.user.email)
        phone=request.POST.get("phone",request.user.phone_no)
        gender=request.POST.get("gender",request.user.gender)
        location=request.POST.get("location")
        age=request.POST.get("age",request.user.age)
        address=request.POST.get("address",request.user.address)
        dob=request.POST.get("dob",request.user.address)
        print("---------",dob)
        try:
            c=city.objects.get(id=int(location))
        except:
            messages.error(request,"Please Update every field")
        if bool(firstname)==False or bool(lastname)==False or bool(phone)==False:
            messages.error(request,"Please Update every field") 
        else:
            a=User.objects.get(email=request.user.email)
            try:
                try:
                    dobstrp = datetime.datetime.strptime(dob, '%Y-%m-%d')
                except:
                    dobstrp = datetime.datetime.strptime(dob, '%d-%m-%Y')
                a.first_name=firstname
                a.last_name=lastname
                a.photo=profilepic
                # a.username=name
                a.email=email
                a.phone_no=phone
                a.gender=gender
                a.location=c
                a.age=age
                a.address=address
                a.dob=dobstrp
                a.save()
                messages.success(request,"Profile updated Successfully")
            except Exception as e:
                print("-----------",e)
                messages.error(request,"Please Update every field")
        return redirect("profile")  
             
def userLogin(request):
    # try :
    #     if request.session.get('failed') > 2:
    #         return HttpResponse('<h1> You have to wait for 5 minutes to login again</h1>')
    # except:
    #     request.session['failed'] = 0
    #     request.session.set_expiry(100)
    if request.method == "POST":
        username = request.POST['email']
        request.session["emaill"]=username
        password = request.POST['password']
        remind=request.POST.get('remindme')
        try:
            a=User.objects.get(email=username)
            user = authenticate(request,username=username,password=password)
            a=request.session.get("cartt")
            if user is not None:
                if remind=='on':
                    settings.SESSION_COOKIE_AGE=2630000  
                login(request,user)
                a=request.session.get("cartt")
                city=request.session.get("city")
                try:
                    chckupp=healthcheckuppackages.objects.filter(id__in=a.get("checkup"))
                except:
                    pass
                try:
                    package=healthpackages.objects.filter(id__in=a.get("package"))
                except:
                    pass
                try:
                    tessst=test.objects.filter(id__in=a.get("selecttest"))
                except:
                    pass
                
                try:
                    for j in chckupp:
                        
                        if city==Bangalore:
                            price=str(j.dBanglore_price)
                        
                        elif city == Mumbai:
                            price=str(j.dMumbai_price)
                        
                        elif city == Bhophal:
                            price=str(j.dbhopal_price)
                        
                        elif city == Nanded:
                            price=str(j.dnanded_price)
                            
                        elif city == Pune:
                            price=str(j.dpune_price)
                        
                        elif city == Barshi:
                            price=str(j.dbarshi_price)
                        
                        elif city == Aurangabad:
                            price=str(j.daurangabad_price)
                            
                        cart.objects.create(user=request.user,labtest=j,price=price).save()
                except:
                    pass   
                try:    
                    for j in package:
                        
                        if city==Bangalore:
                            price=str(j.Banglore_price)
                        
                        elif city == Mumbai:
                            price=str(j.Mumbai_price)
                        
                        elif city == Bhophal:
                            price=str(j.bhopal_price)
                        
                        elif city == Nanded:
                            price=str(j.nanded_price)
                            
                        elif city == Pune:
                            price=str(j.pune_price)
                        
                        elif city == Barshi:
                            price=str(j.barshi_price)
                        
                        elif city == Aurangabad:
                            price=str(j.daurangabad_price)
                        cart.objects.create(user=request.user,packages=j,price=price).save()
                except:
                    pass   
                try:    
                    for j in tessst:
                        if city==Bangalore:
                            price=str(j.Banglore_price)
                        
                        elif city == Mumbai:
                            price=str(j.Mumbai_price)
                        
                        elif city == Bhophal:
                            price=str(j.bhopal_price)
                        
                        elif city == Nanded:
                            price=str(j.nanded_price)
                            
                        elif city == Pune:
                            price=str(j.pune_price)
                        
                        elif city == Barshi:
                            price=str(j.barshi_price)
                        
                        elif city == Aurangabad:
                            price=str(j.daurangabad_price)
                        cart.objects.create(user=request.user,items=j,price=price,categoryy=j.categoryy).save()
                except:
                    pass
                request.session['cart_count']= cart.objects.filter(user =user).count()
                next = request.POST.get('next', '/')
                return HttpResponseRedirect(next)  
                # return redirect('/')
            else:
                messages.error(request,'Invalid Password')
        except:
            messages.error(request,'Email ID is not registered')
    return render(request,'login.html')

def booktestonline(request):
    return render(request,"book-test-online.html")
def logout_request(request):
    logout(request)
    request.session.delete("city")
    request.session.delete("cartt")
    return redirect("/")
def newsletter(request):
    if request.method=="POST":
        email=request.POST["email"]
        data=subscription.objects.filter(email=email)
        if data.exists():
            return JsonResponse({"message":False})
        subscription.objects.create(email=email).save()
        return JsonResponse({"message":True,"email":email})
    # return render(request,"footer.html")
def home(request):
    # request.session["city"]="Bangalore"
    # request.session["city"]="Bangalore"
    deviceCookie = request.COOKIES.get('device')
    c=request.session.get("city")
    envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
    if request.method =="GET":
        cit=city.objects.filter(active=True)
        # tests=test.objects.select_related("categoryy").all()
        healthcheckup=healthcheckuppackages.objects.all()
        healthpackage=healthpackages.objects.prefetch_related("test_name").all()
        healthsymptom=healthsymptoms.objects.prefetch_related("test_name").all()
        healthcareblog=healthcareblogs.objects.prefetch_related("category").all()
        testimonial=testimonials.objects.all()
        # for i in healthsymptom:
        #     print(i.name)
        context={
            "healthcheckup":healthcheckup,
            "healthpackage":healthpackage,
            "healthsymptom":healthsymptom,
            "testimonial":testimonial,
            "healthcareblog":healthcareblog,
            "city":cit,
            "currentcity":c,
            # "tests":tests,
            "envcity":envcity,
            "blogcount":healthcareblog.count(),
            "testimonialcount":testimonial.count(),
        }
        if not request.user.is_anonymous:
            usercart = cart.objects.filter(user=request.user)
        else:
            devicecart = cart.objects.filter(device=deviceCookie)    
        if request.user.is_anonymous:
            request.session['cart_count']= cart.objects.filter(device=deviceCookie).count()
        else:
            if cart.objects.filter(user = request.user).count()==0:
                request.session['cart_count']= cart.objects.filter(device=deviceCookie).count()
            else:
                request.session['cart_count']= cart.objects.filter(user=request.user).count()
        res = render(request,'home.html',context)
        return res

    if request.method=="POST":
        firtname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        message1=request.POST["message"]
        requestcall.objects.create(firstname=firtname,lastname=lastname,phone=phone,email=email,message=message1).save()
        message = f'Hi\nYou have Call back request\nFull Name:{firtname} {lastname}\nMobile:{phone}\nEmail:{email}\nMessage:{message1}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["enquiry@spanhealth.com"]
        message = message
        subject = "Request Call back"
        # send_mail(
        #             subject,
        #             message,
        #             email_from,
        #             recipient_list,
        #             fail_silently=False,
        #     )
        AdminEmailThread(subject, message, reachus).start()
        # cit=city.objects.all()
        # tests=test.objects.all()
        # healthcheckup=healthcheckuppackages.objects.all()[0:4]
        # healthpackage=healthpackages.objects.all()
        # healthsymptom=healthsymptoms.objects.all()
        # healthcareblog=healthcareblogs.objects.all()
        # testimonial=testimonials.objects.all()
        # context={
        #         "healthcheckup":healthcheckup,
        #         "healthpackage":healthpackage,
        #         "healthsymptom":healthsymptom,
        #         "testimonial":testimonial,
        #         "healthcareblog":healthcareblog,
        #         "city":cit,
        #         "currentcity":c,
        #         "tests":tests,
        #         "envcity":envcity,
        # }
        messages.success(request,"Submitted Successfully")
        return HttpResponseRedirect(reverse("home"))

def healthcheckupview(request,slug):
    c=request.session.get("city")
    city="Hyderabad"
    data=healthcheckuppackages.objects.select_related("test_name").filter(slug=slug)[0:4]
    context={
        "data":data,
        "city":city
    }
    return render(request,'dummy.html',context)

def healthcheckupallview(request):
    c=request.session.get("city")
    checkups=healthcheckuppackages.objects.select_related("test_name").all()
    context={
        "checkups":checkups,
        "currentcity":c
    }
    return render(request,'latestviewall.html',context)
def hpackagess(request):
    packages=healthpackages.objects.select_related("test_name").all()
    cit=request.session.get("city")
    envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
    context={
        "packages":packages,
        "city":cit,
        "envcity":envcity,
    }
    return render(request,'healthpackages.html',context)

def healthpackageview(request,slug):
        citi=request.session.get("city")
        package=healthpackages.objects.select_related("test_name").get(slug=slug)
        packages=healthpackages.objects.select_related("test_name").exclude(slug=slug)
        tests=package.test_name.all()
        c=package.test_name.all().count()
        l=int(c)//2
        a,b=tests[:l],tests[l:]
        lstt=[]
        for (a, b) in itertools.zip_longest(a, b,fillvalue=None):
            # print(a.testt,b.testt, end="--")
            if a != None:
                item1=a.testt
            else:
                item1=None
            if b != None:    
                item2=b.testt
            else:
                item2=None
            lis=[item1,item2]
            lstt.append(lis) 
        
        # for i in range(c):
        #     # print(tests[i].testt)
        #     try:
        #         item1=tests[j].testt
        #         item2=tests[i+1].testt
        #         j=i+1
        #         lis=[item1,item2]
        #         lstt.append(lis)
        #     except:
        #         pass
        # print(lstt)
            
        envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
        context={
            "package":package,
            "packages":packages,
            "city":citi,
            'envcity':envcity,
            "firsthalf":a,
            "secondhalf":b,
            "tesst":lstt
        }
        # currency = 'INR'
        # if c == Bangalore:
        #     amount=int(package.Banglore_price)
        # elif c == Mumbai:
        #     amount=int(package.Mumbai_price)
        # elif c == Bhophal:
        #     amount=int(package.bhopal_price)
        # elif c == Nanded:
        #     amount=int(package.nanded_price)
        # elif c == Pune:
        #     amount=int(package.pune_price)
        # elif c == Barshi:
        #     amount=int(package.barshi_price)
        # elif c == Aurangabad:
        #     amount=int(package.aurangabad_price)
        # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        # try:
        #     razorpay_order = client.order.create(
        #             {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        #     )
        # except Exception as e:
        #     razorpay_order = client.order.create(
        #             {"amount": 1* 100, "currency": "INR", "payment_capture": "1"}
        #     )
        # # request.session['amount']=amount
        # razorpay_order_id = razorpay_order['id']
        
        # # callback_url = callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
        # context['razorpay_order_id'] = razorpay_order_id
        # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        # # context['razorpay_amount'] = amount
        # context['currency'] = currency
        return render(request,'packagedetail.html',context)
def testdetails(request):
    if request.method=="POST":
            id=request.POST["id"]
            a=book_history.objects.select_related("user").get(id=id)
            return JsonResponse({"message":a.bookingdetails})
def prescriptionbreak(request):
    if request.method=="POST":
        city=request.session.get("city")
        id=request.POST["id"]
        a=Prescriptionbook1.objects.prefetch_related("test_name").get(bookingid=id)
        if a.coupon == None:
            strr=[]
            for i in a.test_name.all():
                di={}
                di["test"]=(i.testt)
                if city == Bangalore:
                    di["pricel1"]=str(i.Banglore_price)
                elif city== Mumbai:
                    di["pricel1"]=str(i.Mumbai_price)
                elif city== Bhophal:
                    di["pricel1"]=str(i.bhopal_price)
                elif city== Nanded:
                    di["pricel1"]=str(i.nanded_price)
                elif city== Pune:
                    di["pricel1"]=str(i.pune_price)
                elif city== Barshi:
                    di["pricel1"]=str(i.barshi_price)
                elif city== Aurangabad:
                    di["pricel1"]=str(i.aurangabad_price)
                strr.append(di)
            # listToStr = '/'.join(map(str, strr))
            return JsonResponse({"message":strr,"coupon":False})
        else:
            try:
                redeem=couponredeem.objects.select_related("user").get(booking_id=id)
                strr=[]
                for i in a.test_name.all():
                    di={}
                    di["test"]=(i.testt)
                    if city == Bangalore:
                        di["pricel1"]=str(i.Banglore_price)
                    elif city== Mumbai:
                        di["pricel1"]=str(i.Mumbai_price)
                    elif city== Bhophal:
                        di["pricel1"]=str(i.bhopal_price)
                    elif city== Nanded:
                        di["pricel1"]=str(i.nanded_price)
                    elif city== Pune:
                        di["pricel1"]=str(i.pune_price)
                    elif city== Barshi:
                        di["pricel1"]=str(i.barshi_price)
                    elif city== Aurangabad:
                        di["pricel1"]=str(i.aurangabad_price)
                    strr.append(di)
                # listToStr = '/'.join(map(str, strr))
                return JsonResponse({"message":strr,"couponcode":a.coupon.couponcode,"coupon":True,"coupondiscount":redeem.discountpercen,"discountamount":redeem.discountamount})
            except Exception as e:
                print(e)
                # redeem=couponredeem.objects.get(booking_id=id)
                strr=[]
                for i in a.test_name.all():
                    di={}
                    di["test"]=(i.testt)
                    if city == Bangalore:
                        di["pricel1"]=str(i.Banglore_price)
                    elif city== Mumbai:
                        di["pricel1"]=str(i.Mumbai_price)
                    elif city== Bhophal:
                        di["pricel1"]=str(i.bhopal_price)
                    elif city== Nanded:
                        di["pricel1"]=str(i.nanded_price)
                    elif city== Pune:
                        di["pricel1"]=str(i.pune_price)
                    elif city== Barshi:
                        di["pricel1"]=str(i.barshi_price)
                    elif city== Aurangabad:
                        di["pricel1"]=str(i.aurangabad_price)
                    strr.append(di)
                # listToStr = '/'.join(map(str, strr))
                return JsonResponse({"message":strr,"couponcode":a.coupon.couponcode,"coupon":True})
def healthsymptomview(request,slug):
    deviceCookie = request.COOKIES.get('device')
    c=request.session.get("city")
    data=healthsymptoms.objects.prefetch_related("test_name").filter(slug=slug)
    
    context={
        "data":data,
        "city":c,
    }
    return render(request,'',context)
def healthcareblogsview(request,slug):
    c=request.session.get("city")
    detail=healthcareblogs.objects.select_related("category").get(slug=slug)
    blogs=healthcareblogs.objects.select_related("category").all().order_by("-created")
    category=blogcategory.objects.all()
    context={
        "detail":detail,
        "blogs":blogs, 
        "category":category,
    }
    return render(request,'blogdetail.html',context)
def categoryblog(request,slug):
    detail=healthcareblogs.objects.select_related("category").first()
    blogs=healthcareblogs.objects.select_related("category").filter(category__slug=slug).order_by("-created")
    category=blogcategory.objects.all()
    context={
        "detail":detail,
        "blogs":blogs, 
        "category":category,
    }
    return render(request,'blogdetail.html',context)
@login_required(login_url="/login/")   
def prescriptionbookview(request):
    # if request.user.is_anonymous:
    #     # return redirect("user-login")
    #     return HttpResponseRedirect(reverse("user-login"))
    # else:
    c=request.session.get("city")
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("user-login"))
    if request.method=="POST":
        prescription_file=request.FILES.get("file")
        myself=request.POST.get("radio_self")
        others=request.POST.get('radio_others')
        others_choice=request.POST.get("option")
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        contact=request.POST.get('phone')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        address=request.POST.get("address")
        unique = uuid.uuid4()
        s = shortuuid.ShortUUID(alphabet="0123456789")
        bid = s.random(length=5)
        # bookingid="DP"+str(bid)
        book=book_history.objects.filter(user=request.user).order_by("-created")[0:1]
        for i in book:
            temp = re.compile("([a-zA-Z]+)([0-9]+)")
            res = temp.match(i.bookingid).groups()
        try: 
            booking=int(res[1])+1
            if str(booking)==str(bid):
                bookingid="DP"+str(bid)
            else:    
                bookingid="DP"+str(booking)
        except:
            bookingid="DP"+str(bid)
        # prescription_book(
        #     user=request.user,
        #     unique=unique,
        #     prescription_file=prescription_file,
        #     myself=True if myself == "on" else False,
        #     others=True if others == "on" else False,
        #     others_choice=others_choice,
        #     firstname=firstname,
        #     lastname=lastname,
        #     contact=contact,
        #     age=age,
        #     gender=gender,
        #     location=c,
        #     address=address).save()
        
        Prescriptionbook1(
            user=request.user,
            unique=unique,
            prescription_file=prescription_file,
            myself=True if myself == "on" else False,
            others=True if others == "on" else False,
            others_choice=others_choice,
            firstname=firstname,
            lastname=lastname,
            contact=contact,
            age=age,
            gender=gender,
            location=c,
            address=address,
            bookingid=bookingid).save()
        data2=Prescriptionbook1.objects.prefetch_related("test_name").get(unique=unique)
        if myself=="on":
            User.objects.filter(email=request.user.email).update(first_name=firstname,last_name=lastname,phone_no=contact,age=age,address=address,gender=gender)
        # data=prescription_book.objects.get(unique=unique)
        book_history(
            user=request.user,
            testbooking_id=data2.id,
            uni=data2.bookingid,
            bookingid=bookingid,
            patient_info="myself" if others==None else "others",
                    booking_type="Prescription",
                    bookingdetails="upload prescription",
                    payment_status=False).save()
        
        messages.success(
            request, "Thankyou for your booking!, Our admin team will get back to you shortly.")
        link=request.build_absolute_uri('/booking-history')
        message=f'Hello {request.user.first_name},\n You have successfully uploaded your prescription on our website, our internal team will review it and get back to you shortly for further steps.\nYou can always track your bookings/uploads (link: {link})\n\nWe appreciate your patience\nThank You,\nDIAGNOSTICA SPAN'
            # message = f'Welcome your otp is {otp} '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        subject = "Prescription Upload Successfull | DIAGNOSTICA SPAN" 
        # send_mail(
        #         subject,
        #         message,
        #         email_from,
        #         recipient_list,
        #         fail_silently=False,
        # )
        msg=f"Hi\nThere is an Upload Prescription order booked with following details\nBooking ID:{bookingid}\nFullname:{firstname} {lastname}\nLocation:{c}\nPhone Number:{contact}"
        # send_mail(
        #     subject,
        #     msg,
        #     email_from,
        #     reachus,
        #     fail_silently=False,
        #           )
        # msg=f"Hi\nThere is an Upload Prescription order booked with following details\nBookingID:{bookingid}\nFullname:{firstname}{lastname}\nLocation={c}\nPhone Number:{contact}"
        # number=8105486993
        # sms(msg,number)
        customerEmailThread(subject, message, recipient_list).start()
        AdminEmailThread(subject, msg, reachus).start()
        return HttpResponseRedirect(reverse("booking-history"))
    else:
        return render(request,"uploadprescriptions.html")
        
# @login_required(login_url="login/")  
def testselect(request):
    deviceCookie = request.COOKIES['device']
    c=request.session.get("city")
    tcategories=category.objects.all()
    tests=test.objects.select_related("categoryy").filter(Banglore_price__isnull=False)
    envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
    if request.user.is_anonymous:
        carts=cart.objects.select_related("user").filter(device = deviceCookie)
    else:
        carts=cart.objects.select_related("user").filter(user = request.user)
    cartlist=[]
    for carrt in carts:
        try:
           cartlist.append(int(carrt.items.id)) 
        except:
            pass
    context={
        "tests":tests,
        "categories":tcategories,
        "city":c,
        'envcity':envcity,
        "cartlist":cartlist
    }
    # if request.method=="POST":
    #     test_name=request.POST.getlist("test_name")
    #     myself=request.POST.get("myself")
    #     others=request.POST.get('others')
    #     others_choice=request.POST.get("others_choice")
    #     firstname=request.POST.get('firstname')
    #     lastname=request.POST.get('lastname')
    #     contact=request.POST.get('contact')
    #     age=request.POST.get('age')
    #     gender=request.POST['gender']
    #     unique = uuid.uuid4()
    #     s = shortuuid.ShortUUID(alphabet="0123456789")
    #     bid = s.random(length=5)
    #     bookingid="DP"+str(bid)
    #     for i in test_name:
    #         item=test.objects.get(id=i)
    #         if c==Bangalore:
    #             cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.Banglore_price).save()
    #         elif c == Mumbai:
    #             cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.Mumbai_price).save()
    #         elif c == Bhophal:
    #             cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.bhopal_price).save()   
    #         elif c == Nanded:
    #             cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.nanded_price).save()
    #         elif c == Pune:
    #             cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pune_price).save()
    #         elif c == Barshi:
    #             cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.barshi_price).save()   
    #         elif c == Aurangabad:
    #             cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.aurangabad_price).save()
    #     messages.success(request,"Your booking added to cart successfully")
    #     return render(request,"choose-test-list.html",context)
    return render(request,"choose-test-list.html",context)

def couponsessiondelete(request):
    coupon=request.session.get("coupon")
    discountamount=request.session.get("discountamount")
    couponpercent=request.session.get("couponpercent")
    actualamount= request.session.get("actualamount")
    if coupon!=None:
            del request.session['coupon']
    if discountamount!=None:
        del request.session['discountamount']
    if couponpercent!=None:
        del request.session['couponpercent']
    if actualamount!=None:
        del request.session['actualamount']
    return JsonResponse({"message":True})
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def cartt(request):
    deviceCookie = request.COOKIES.get('device')
    cit=city.objects.filter(active=True)
    if not request.user.is_anonymous:
        d = cart.objects.select_related("user").filter(device = deviceCookie).update(user=request.user)
    if request.method=="POST":
        c=request.session.get("city")
        others=request.POST.get('option1')
        others_choice=request.POST.get("option")
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        contact=request.POST.get('phone')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        address=request.POST['address']
        timeslot=request.POST.get('timeslot')
        date=request.POST.get('date')
        location=request.POST.get('location')
        pincode=request.POST.get('pincode')
        landmark=request.POST.get("landmark")
        amount=request.POST["amount"]
        dob=request.POST.get("dob")
        global uniquee
        uniquee = uuid.uuid4()
        data=cart.objects.filter(user=request.user)
        s = shortuuid.ShortUUID(alphabet="0123456789")
        bid = s.random(length=5)
        book=book_history.objects.select_related("user").all().order_by("-created")[0:1]
        for i in book:
            temp = re.compile("([a-zA-Z]+)([0-9]+)")
            res = temp.match(i.bookingid).groups()
            print(res[1])
        try: 
            booking=int(res[1])+1
            if str(booking)==str(bid):
                bookingid="DP"+str(bid)
            else:    
                bookingid="DP"+str(booking)
        except:
            bookingid="DP"+str(bid)
        data1=cart.objects.select_related("user").filter(user=request.user)
        tes=[]
        testli=[]
        for i in data1:
            dic={}
            dicc={}
            if i.items:
                a=dic["tests_code"]=i.items.testcode
                dicc["testCode"]=i.items.testcode
                testli.append(dicc)
                tes.append(dic)
                # print("-----------",i.items.testcode)
            if i.packages:
                for j in i.packages.test_name.all():
                    a=dic["tests_code"]=j.testcode
                    dicc["testCode"]=j.testcode
                    testli.append(dicc)
                    tes.append(dic)
                    # print(i.testcode)
            if i.labtest:
                a=dic["tests_code"]=i.labtest.code
                dicc["testCode"]=i.labtest.code
                testli.append(dicc)
                tes.append(dic)
                # print("---------",i.labtest.code)
            if i.healthsymptoms:
                for j in i.healthsymptoms.test_name.all():
                    a=dic["tests_code"]=j.testcode
                    dicc["testCode"]=j.testcode
                    testli.append(dicc)
                    tes.append(dic)
                    # print(i.testcode)
        # print(tes)
        if gender=="m":
            genderr="Male"
        elif gender == "f":
            genderr="Female"
        else:
            genderr="Other"
        coup=request.session.get("coupon")
        couponper=request.session.get("couponpercent")
        if couponper!=None:
            perc=str(couponper)
        else:
            perc="0"
        if coup!=None:
            coupo=str(coup)
        else:
            coupo="-"
        url = "https://mtqn0qowxc.execute-api.us-east-1.amazonaws.com/create-customer-order"
        payload = json.dumps({
          "order_ref_id": bookingid,
          "lab_code": "DIASPAN",
          "patient_address": address,
          "patient_pincode": pincode,
          "patient_phone": contact,
          "altphone": contact,
          "date": date,
          "slot": timeslot,
          "patient_email": request.user.email,
          "patient_landmark": landmark,
          "payment_type": "Prepaid",
          "total_amount": amount,
          "discount_type": "Percentage",
          "discount_value": perc,
          "payment_amount":amount,
          "advance_paid": amount,
          "payment_to_collect": "0",
          "is_test": 1,
          "patients": [
            {
              "patient_ref_id": "null",
              "first_name": firstname,
              "last_name": lastname,
              "gender": genderr,
              "age": age,
              "remark": "",
              "tests":tes
            }
          ]
        })
        headers = {
          'api-key': gosamplify_apikey,
          'customer-code': customer_code,
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(json.loads(response.text))
        res=json.loads(response.text)
        # print("----",response.status_code)
        if response.status_code==201:
            cc=location.split(',')
            cit=city.objects.get(id=int(cc[0]))
            citname=cit.cityname
            gosamporderid=res["data"][0]["order_number"]
            gosamtaskid=res["data"][0]["task_id"]
            tokencity=request.session.get("tempcity")
            appointres=appointment(testli,firstname,lastname,age,genderr,gosamporderid,citname,dob,tokencity)
            print("------------",json.loads(appointres))
            appointress=json.loads(appointres)
            if appointress["code"]==200:
                creliohealthdata.objects.create(organisationid=appointress["organisationid"],billid=appointress["billid"],spanbookingid=bookingid,gosamplifyorderid=gosamporderid,gosamplifytaskid=gosamtaskid,labtoken=appointress["labtoken"]).save()
                goordernumber=res["data"][0]["order_number"]
                taskid=res["data"][0]["task_id"]
                orderref=res["data"][0]["order_ref_number"]
                slotdate=res["data"][0]["slot_date"]
                slottime=res["data"][0]["slot_time"]
                amountt=res["data"][0]["amount_to_collect"]
                patientname=res["data"][0]["main_patient_name"]
                email=res["data"][0]["patient_email"]
                phone=res["data"][0]["patient_phone"]
                addres=res["data"][0]["patient_address"]
                pincodee=res["data"][0]["patient_pincode"]
                status=res["data"][0]["status"]
                payment_type=res["data"][0]["payment_type"]
                price_=res["data"][0]["amount_to_collect"]
                gosamplify.objects.create(
                        goordernumber=goordernumber,taskid=taskid,orderref=orderref,paymenttype=payment_type,price=amount,couponval=perc,couponcode=coupo,slotdate=slotdate,slottime=slottime,amountt=amountt,patientname=patientname,email=email,phone=phone,address=addres,pincode=pincodee,status=status
                    ).save()
                if others=="m":
                    User.objects.filter(email=request.user.email).update(first_name=firstname,last_name=lastname,phone_no=contact,age=age,address=address,gender=gender)
                # data1=cart.objects.filter(user=request.user)
                request.session.delete("order_id")
                context={}
                currency = 'INR'
                client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                try:
                    razorpay_order = client.order.create(
                        {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
                    )
                except:
                    razorpay_order = client.order.create(
                            {"amount": 1* 100, "currency": "INR", "payment_capture": "1"}
                    )
                request.session["order_id"]=razorpay_order['id']
                razorpay_order_id = razorpay_order['id']
                callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
                # print("----------------",callback_url)
                # print(call)
                # print(callback_url)
                # callback_url = 'https://spandiagno.com/paymenthandler/{}/{}/'.format(request.user.email,amount)
                context['razorpay_order_id'] = razorpay_order_id
                context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                context['razorpay_amount'] = amount
                context['currency'] = currency
                context['callback_url'] = callback_url
                strr=[]
                for tesst in data1:
                    if tesst.packages:
                        strr.append(tesst.packages.package_name)
                        invoicee.objects.create(user=request.user,order_id=razorpay_order_id,packages=tesst.packages,price=tesst.price).save()
                    elif tesst.labtest:
                        strr.append(tesst.labtest.package_title)
                        invoicee.objects.create(user=request.user,order_id=razorpay_order_id,labtest=tesst.labtest,price=tesst.price).save()
                    elif tesst.healthsymptoms:
                        strr.append(tesst.healthsymptoms.name)
                        invoicee.objects.create(user=request.user,order_id=razorpay_order_id,healthsymptoms=tesst.healthsymptoms,price=tesst.price).save()
                    elif tesst.items: 
                        strr.append(tesst.items.testt)
                        invoicee.objects.create(user=request.user,order_id=razorpay_order_id,items=tesst.items,price=tesst.price).save()       
                listToStr = '/'.join(map(str, strr))
                listToline = '\n /'.join(map(str, strr))
                
                a=testbook.objects.create(
                        unique=uniquee,
                        user=request.user,
                        tests=listToline,
                        myself=True if others == "m" else False,
                        others=True if others == "o" else False,
                        others_choice=others_choice,
                        firstname=firstname,
                        lastname=lastname,
                        contact=contact,
                        age=age,
                        gender=gender,
                        locationn=cit,
                        pincode=pincode,
                        date=date,
                        address=address,
                        landmark=landmark,
                        timeslot=timeslot,
                        bookingid=bookingid,)
                data=testbook.objects.select_related("user").get(unique=uniquee) 
                bookhistory=book_history(
                         user=request.user,
                         testbooking_id=data.id,
                         uni=data.bookingid,
                         bookingid=bookingid,
                         patient_info="Myself" if others == "m" else "others",
                                 booking_type="Selected Test/Packages",
                                 bookingdetails=listToStr,
                                 amount="{0:1.2f}".format(float(amount)),
                                 payment_id=razorpay_order_id,
                                 payment_status=False).save()
                # msg=f"Hi\nThere is an Prescription Upload order booked with below details\nBookingID:{bookingid}\nFirstname:{firstname}\nLastname:{lastname}\n"
                # number=###
                # sms(msg,number)
                # for i in data1:
                #     print(i.items)
                #     print(i.labtest)
                #     print(i.packages)
                #     print(i.healthsymptoms)
                #     if i.items==None and i.labtest==None and i.packages==None and i.healthsymptoms!=None:
                #         print(1)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health Symptoms",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items!=None and i.labtest==None and i.packages==None and i.healthsymptoms==None:
                #         print(2)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Selected Test",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items==None and i.labtest!=None and i.packages==None and i.healthsymptoms==None:
                #         print(3)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health checkups",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items==None and i.labtest==None and i.packages!=None and i.healthsymptoms==None:
                #         print(4)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health Packages",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items==None and i.labtest==None and i.packages!=None and i.healthsymptoms!=None:
                #         print(5)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health Packages/Symptoms",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items==None and i.labtest!=None and i.packages==None and i.healthsymptoms!=None:
                #         print(6)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health Checkups/Symptoms",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items!=None and i.labtest==None and i.packages==None and i.healthsymptoms!=None:
                #         print(7)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Selected Test/Symptoms",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items!=None and i.labtest==None and i.packages!=None and i.healthsymptoms==None:
                #         print(8)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Selected Test/Packages",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()

                #     elif i.items!=None and i.labtest!=None and i.packages==None and i.healthsymptoms==None:
                #         print(9)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Selected Test/Checkups",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()

                #     elif i.items==None and i.labtest!=None and i.packages!=None and i.healthsymptoms==None:
                #         print(10)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health Chekups/Packages",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items!=None and i.labtest!=None and i.packages!=None and i.healthsymptoms!=None:
                #         print(11)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health Chekups/Packages",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items==None and i.labtest!=None and i.packages!=None and i.healthsymptoms!=None:
                #         print(12)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Health Chekups/Packages/Symptoms",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     elif i.items!=None and i.labtest==None and i.packages!=None and i.healthsymptoms!=None:
                #         print(13)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Selected Test/Packages/Symptoms",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()

                #     elif i.items!=None and i.labtest!=None and i.packages==None and i.healthsymptoms!=None:
                #         print(14)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Selected Test/Symptoms/Health Checkups",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()

                #     elif i.items!=None and i.labtest!=None and i.packages==None and i.healthsymptoms!=None:
                #         print(15)
                #         bookhistory=book_history(
                #             user=request.user,
                #             testbooking_id=data2.id,
                #             bookingid=bookingid,
                #             patient_info="Myself" if others == "m" else "others",
                #                     booking_type="Selected Test/Symptoms/Health Checkups",
                #                     bookingdetails=listToStr,
                #                     amount="{0:1.2f}".format(float(amount)),
                #                     payment_id=razorpay_order_id,
                #                     payment_status=False).save()
                #     else:
                #         print(16)
                #         bookhistory=book_history(
                #          user=request.user,
                #          testbooking_id=data2.id,
                #          bookingid=bookingid,
                #          patient_info="Myself" if others == "m" else "others",
                #                  booking_type="Items",
                #                  bookingdetails=listToStr,
                #                  amount="{0:1.2f}".format(float(amount)),
                #                  payment_id=razorpay_order_id,
                #                  payment_status=False).save()

                coupon=request.session.get("coupon")
                discountamount=request.session.get("discountamount")
                couponpercent=request.session.get("couponpercent")
                actualamount= request.session.get("actualamount")

                if coupon!= None and discountamount!=None and couponpercent!=None and actualamount!=None:
                     couponredeem.objects.create(user=request.user,booking_id=data.bookingid,order_id=razorpay_order_id,coupon=request.session.get("coupon"),discountpercen=request.session.get("couponpercent"),discountamount=request.session.get("discountamount"),actualamount=request.session.get('actualamount')).save()
                if coupon!=None:
                    del request.session['coupon']
                if discountamount!=None:
                    del request.session['discountamount']
                if couponpercent!=None:
                    del request.session['couponpercent']
                if actualamount!=None:
                    del request.session['actualamount']
                # print(razorpay_order)
                # messages.info(request,"Please Login to checkout")
                return JsonResponse({"message":True,"razorpay_key":settings.RAZOR_KEY_ID,"currency":currency,"razorpayorder":razorpay_order_id,"callback":callback_url})
            else:
                tid=res["data"][0]["task_id"]
                url = f"https://mtqn0qowxc.execute-api.us-east-1.amazonaws.com/delete-customer-visit/{tid}"
                payload={}
                headers = {
                  'api-key': gosamplify_apikey,
                  'customer-code': customer_code,
                'Content-Type': 'application/json'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                # gos=gosamplify.objects.filter(orderref=d.bookingid)
                return JsonResponse({"message":False})
        elif response.status_code==401:
            subject=f"401 Unauthorised for Go Samplify"
            message=f"Hi There,\nGo Samplify Order Creating API is Getting Unauthorised Error,Error Code :401\nPlease Lookinto it"
            AdminEmailThread(subject, message, reachus).start()
            return JsonResponse({"message":False})
        else:
            return JsonResponse({"message":False})
    if not request.user.is_anonymous:
        c = cart.objects.select_related("user").filter(user=request.user)
    else:
        c = cart.objects.select_related("user").filter(device=deviceCookie)
    data=[]
    for i in c:
        if i.items == None and i.labtest:
            da={}
            da['id']=i.id
            da['test']=i.labtest
            da['price']=str(i.price)
            da["categoryy"]="Popular Tests"
            data.append(da)
        elif i.items == None and i.packages:
            da={}
            da['id']=i.id
            da['test']=i.packages
            da['price']=str(i.price)
            da["categoryy"]="Packages"
            data.append(da)
        elif i.healthsymptoms:
            da={}
            da['id']=i.id
            da['test']=i.healthsymptoms.name
            da['price']=str(i.price)  
            da["categoryy"]="Life Style Assessments"
            data.append(da)
        elif i.items: 
            da={}
            da['id']=i.id
            da['test']=i.items
            da['price']=str(i.price)  
            da["categoryy"]=i.items.categoryy
            data.append(da)
    try: 
        a=[float(i["price"]) for i in data]
        total=float('{0:1.2f}'.format(sum(a)))+shipping_charges
        # print(float('{0:1.2f}'.format(sum(a)))+199)
        context={
            "city":cit,
            "data":data,
            "datacount":len(data),
            "subtotal": '{0:1.2f}'.format(sum(a)),
            "total":total
        }
    except Exception as e:
         context={
            "city":cit,
            "data":data,
            "datacount":len(data),
        }
    
    if request.user.is_anonymous:
        request.session['cart_count']= cart.objects.filter(device = deviceCookie).count()
    else:
        request.session['cart_count']= cart.objects.filter(user = request.user).count()
    return render(request,"mycart.html",context)
        # except:
        #     return render(request,"mycart.html")
 
def cartsessiondelete(request):
    deviceCookie = request.COOKIES['device']
    if request.method=="POST":
        to_del=request.POST["pk"]
        objs = cart.objects.get(
           Q(device=deviceCookie, id = to_del)|
           Q(user=request.user if not request.user.is_anonymous else None, id = to_del)
            ).delete()
        if request.user.is_anonymous:
            request.session['cart_count']= cart.objects.filter(device = deviceCookie).count()
        else:
            request.session['cart_count']= cart.objects.filter(user = request.user).count()
        return JsonResponse({"message":True})

def othersdetail(request):
    if request.method=="POST":
        testid=request.POST["testid"]
        print("----",testid)
        try:
            detail=Prescriptionbook1.objects.prefetch_related("test_name").get(bookingid=testid)
            # print("prec")
        except:
            detail=testbook.objects.select_related("user").get(bookingid=testid)
            # print("test")
        choice = ""
        gender=""
        if detail.others_choice=="m":
            choice="Mother"
        elif detail.others_choice=="f":
            choice="Father"
        elif detail.others_choice=="w":
            choice="Wife"
        elif detail.others_choice=="s":
            choice="Son"
        elif detail.others_choice=="d":
            choice="Daughter"
        elif detail.others_choice=="o":
            choice="Other"
        if detail.gender== 'f':
            gender="Female"
        elif detail.gender == 'm':
            gender="Male"
        else:
            gender='Others'
        return JsonResponse({"message":True,"firstname":detail.firstname,"lastname":detail.lastname,"gender":gender,"otherschoice":choice,"age":detail.age,"phone":detail.contact})
@csrf_exempt
def paymenthandler(request,str,amount):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        b = client.utility.verify_payment_signature(response_data)
        request.session['signatureid']=response_data['razorpay_signature']
        # paymentids.objects.create(orderid=response_data['razorpay_order_id'],paymentid=response_data['razorpay_payment_id'],signatureid=response_data['razorpay_signature'])
        return b
    try:
        if request.method =="POST":
            usr=User.objects.get(email=str)
            paymentid=request.POST.get("razorpay_payment_id")
            if paymentid:
                if verify_signature(request.POST):
                    transid=request.POST["razorpay_order_id"]
                    cart.objects.select_related("user").filter(user=usr).delete()
                    history=book_history.objects.select_related("user").get(payment_id=transid)
                    history.payment_status=True
                    Prescriptionbook1.objects.prefetch_related("test_name").filter(bookingid=history.bookingid).update(payment_status=True)
                    testbook.objects.select_related("user").filter(bookingid=history.bookingid).update(payment_status=True)
                    history.save()
                    # signatureid=request.session.get("signatureid")
                    # print("------",signatureid)
                    payment.objects.create(user=usr,paymentid=paymentid,transid=transid,amount=amount,booking_id=history.bookingid).save()
                    # if signatureid!=None:
                    #     del request.session['signatureid']
                    # print("=====",signatureid)
                    request.session.delete("amount")
                    link=request.build_absolute_uri('/booking-history')
                    # message1 = f"Hi there,\nWe have successfully received your payment for booking id: {history.bookingid}.\nOur Medical team will get in touch with you for your mentioned tests.\nClick (link: {link}) to track your bookings.\nThank you\nDIAGNOSTICA Span"
                    email_from = settings.EMAIL_HOST_USER
                    # taskid=gosamplify.objects.get()
                    message1=f"""Hi there,We have successfully received your payment for booking id: {history.bookingid}..\nClick ({link}) to track your bookings.\nThank you\nDIAGNOSTICA SPAN"""
                    recipient_list = [history.user.email]
                    subject = f"Booking Id:{history.bookingid} | Payment Successfull| DIAGNOSTICA Span" 
                    mes=f"Payment is Done for Booking ID:{history.bookingid}\nPlease Checkit"
                    customerEmailThread(subject, message1, [request.user.email]).start()
                    AdminEmailThread(subject, mes, reachus).start()
                    messages.info(request, "Thankyou for making payment our team will come and collect the sample soon.")
                    # return HttpResponseRedirect(reverse("booking-history"))
                    return redirect("booking-history")
                else:
                    messages.error(request, "Payment Failed")
                    # return HttpResponseRedirect(reverse("booking-history"))
                    return redirect("booking-history")
            else:
                transid=request.POST["razorpay_order_id"]
                history=book_history.objects.select_related("user").get(payment_id=transid)
                link=request.build_absolute_uri('/booking-history')
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [history.user.email]
                # subject=f"Subject: Payment Failed| DIAGNOSTICA Span | Booking Id:{history.bookingid}"
                subject=f"Payment Failed| DIAGNOSTICA SPAN | Booking Id:{history.bookingid}"
                message=f"""Hi there,\n
                            The payment initiated for booking id:{history.bookingid} has been failed.\n
                            
                            """
                # send_mail(
                #             f"Payment Failed| DIAGNOSTICA SPAN | Booking Id:{history.bookingid}",
                #             message,
                #             email_from,
                #             recipient_list,
                #             fail_silently=False,
                #     )
                customerEmailThread(subject, message, [history.user.email]).start()
                b=request.POST.get('error[metadata]')
                c=json.loads(b)
                # a=book_history.objects.filter(payment_id=c["order_id"])
                history=book_history.objects.select_related("user").filter(payment_id=c["order_id"])
                Prescriptionbook1.objects.prefetch_related("test_name").filter(bookingid=history.bookingid).delete()
                testbook.objects.select_related("user").filter(bookingid=history.bookingid).delete()
                history.delete()
                error = request.POST.get('error[description]')
                messages.error(request, error)
                # return HttpResponseRedirect(reverse("booking-history"))
                return redirect("booking-history")
        else:
            return redirect("booking-history")
    except Exception as e:
        # print(request.POST["error[metadata]"])
        metadata=request.POST["error[metadata]"]
        print(metadata)
        print(json.loads(metadata))
        a=json.loads(metadata)
        print(a["order_id"])
        # print(metadata[0])
        # print(request.POST.get("order_id"))
        # order_id=request.POST.get(a["order_id"])
        history=book_history.objects.select_related("user").get(payment_id=a["order_id"])
        # for i in history:
        #     a=i.bookingid
        Prescriptionbook1.objects.prefetch_related("test_name").filter(bookingid=history.bookingid).delete()
        testbook.objects.select_related("user").filter(bookingid=history.bookingid).delete()
        history.delete()
        messages.error(request, "Payment failed Please Retry")
        return redirect("booking-history")

def subscriptionview(request):
    if request.method=="POST":
        form=subscriptionform()
        if form.is_valid:
            email=request.POST.get("email")
            template_name = 'email.html'
            msg=EmailMessage(
            'Diagnostica',
            render_to_string(template_name),
            settings.EMAIL_HOST_USER,
            [email],
        )
        msg.content_subtype ="html"
        msg.send()
        messages.success(request,"Thank you for subscribing") 
        return redirect('/')
    else:
        form=subscriptionform
        return render(request,"home",{"form":form})

def addtocart(request):
    cityy=request.session.get("city")
    deviceCookie = request.COOKIES['device']
    RES = {}
    if request.method=="POST":
        pk=request.POST["pk"]
        item=test.objects.get(id=pk)
        if cityy==Bangalore:
            obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                items = item,
                user = request.user if not request.user.is_anonymous else None,
                price=item.Banglore_price,
                )
            res = {"message":created}
            RES = res
            
        elif cityy==Mumbai:
            obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                items = item,
                user = request.user if not request.user.is_anonymous else None,
                price=item.Mumbai_price,
                )
            res = {"message":created}
            RES = res
            
        elif cityy==Bhophal:
            obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                items = item,
                user = request.user if not request.user.is_anonymous else None,
                price=item.bhopal_price,
                )
            res = {"message":created}
            RES = res
            
        elif cityy==Nanded:
            
            obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                items = item,
                user = request.user if not request.user.is_anonymous else None,
                price=item.nanded_price,
                )
            res = {"message":created}
            RES = res
            
        elif cityy==Pune:
            # cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel4).save()
            obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                items = item,
                user = request.user if not request.user.is_anonymous else None,
                price=item.pune_price,
                )
            res = {"message":created}
            RES = res
        
        elif cityy==Barshi:
            # cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel4).save()
            obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                items = item,
                user = request.user if not request.user.is_anonymous else None,
                price=item.barshi_price,
                )
            res = {"message":created}
            RES = res
            
        elif cityy==Aurangabad:
            # cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel4).save()
            obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                items = item,
                user = request.user if not request.user.is_anonymous else None,
                price=item.aurangabad_price,
                )
            res = {"message":created}
            RES = res
           
        if request.user.is_anonymous:
            request.session['cart_count']= cart.objects.filter(device = deviceCookie).count()
        else:
            request.session['cart_count']= cart.objects.filter(user = request.user).count()
        return JsonResponse(RES)
    
def addtocart1(request):
    cityy=request.session.get("city")
    deviceCookie = request.COOKIES['device']
    RES = {}
    if request.method=="POST":
        pk=request.POST.getlist("pk[]")
        item=test.objects.filter(id__in=pk)
        if cityy==Bangalore:
            for i in item:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    items = i,
                    user = request.user if not request.user.is_anonymous else None,
                    price=i.Banglore_price,
                    )
                res = {"message":created}
                RES = res
        if request.user.is_anonymous:
            request.session['cart_count']= cart.objects.filter(device = deviceCookie).count()
        else:
            request.session['cart_count']= cart.objects.filter(user = request.user).count()
        
        return JsonResponse(RES)
def categoryy(request):
    if request.method=="POST":
        city=request.session.get("city")
        pk=request.POST["pk"]
        searched_name = request.POST.get("searched")
        b=[]
        if pk != "all":
            if searched_name:
                tests=test.objects.select_related("categoryy").filter(categoryy__id=pk, testt__icontains = searched_name)
            else:
                tests=test.objects.select_related("categoryy").filter(categoryy__id=pk)
        else:
            tests=test.objects.select_related("categoryy").all()
        for tesst in tests:
            a={}
            a['id']=tesst.id
            a['testt']=tesst.testt
            a['description']=tesst.description
            if city == Bangalore:
                a["pricel1"]=str(tesst.Banglore_price)
            elif city== Mumbai:
                a["pricel1"]=str(tesst.Mumbai_price)
            elif city== Bhophal:
                a["pricel1"]=str(tesst.bhopal_price)
            elif city== Nanded:
                a["pricel1"]=str(tesst.nanded_price)
            elif city== Pune:
                a["pricel1"]=str(tesst.pune_price)
            elif city== Barshi:
                a["pricel1"]=str(tesst.barshi_price)
            elif city== Aurangabad:
                a["pricel1"]=str(tesst.aurangabad_price)
            b.append(a)
        return JsonResponse(b,safe=False)
    
def search(request):
    if request.method=="POST":
        if request.POST.get("action") == "load_more":
            # objs = test.objects.filter().values("testt","description", "pricel1")
            res = {"valid":True}
            return HttpResponse(json.dumps(res), content_type="application/json")
        else:
            city=request.session.get("city")

            searched=request.POST.get('searched')
            req_cat = request.POST.get("cat")
            if req_cat != "all":
                if searched:
                    tests=test.objects.select_related("category").filter(categoryy__id=req_cat, testt__icontains = searched)
                else:
                    tests=test.objects.select_related("category").filter(categoryy__id=req_cat)
            else:
                tests=test.objects.select_related("category").filter(testt__icontains=searched)
            b=[]
            for tesst in tests:
                a={}
                a["id"]=tesst.id
                a["testt"]=tesst.testt
                a["description"]=tesst.description
                if city == Bangalore:
                    a["pricel1"]=str(tesst.Banglore_price)
                elif city== Mumbai:
                    a["pricel1"]=str(tesst.Mumbai_price)
                elif city== Bhophal:
                    a["pricel1"]=str(tesst.bhopal_price)
                elif city== Nanded:
                    a["pricel1"]=str(tesst.nanded_price)
                elif city== Pune:
                    a["pricel1"]=str(tesst.pune_price)
                elif city== Barshi:
                    a["pricel1"]=str(tesst.barshi_price)
                elif city== Aurangabad:
                    a["pricel1"]=str(tesst.aurangabad_price)
                b.append(a)
            return JsonResponse(b,safe=False)
    else:
        return render(request,"choose-test-list.html") 
       
def destroy(request): 
    if request.method=="POST":
        car=request.POST["cart"]
        try:
            a = cart.objects.select_related("user").get(id=car)  
            a.delete()  
        except:
            pass
            # return JsonResponse({"message":True})
        return JsonResponse({"message":"success"})
def coupon(request):
    if request.method=="POST":
        if request.POST.get("action")=="cart":
            coupon=request.POST.get("coupon")
            total=request.POST.get("total")
            citi=request.session.get("tempcity")
            try:
                c=coupons.objects.get(couponcode=coupon,status="active")
                couponcount=couponredeem.objects.select_related("user").filter(coupon=coupon).count()
                if datetime.now(timezone.utc)>c.startdate:
                    if datetime.now(timezone.utc)<c.enddate:
                        if c.cityy.filter(cityname=citi).exists():
                            # if c.limit!=0 or c.limit>0:
                            try:
                                if couponcount<c.limit:
                                    c.discount
                                    discount=(float(total)*(int(c.discount)/100))
                                    totall=(float(total)-int(discount))+shipping_charges
                                    request.session['discountamount']=discount
                                    request.session['coupon']=coupon
                                    request.session['couponpercent']=c.discount
                                    request.session['actualamount']=total
                                    return JsonResponse({"message":True,"total":float(totall),"percent":c.discount,"discount":"{:.2f}".format(discount)})
                                else:
                                    return JsonResponse({"message":False})
                            except:
                                c.discount
                                discount=(float(total)*(int(c.discount)/100))
                                totall=(float(total)-int(discount))+shipping_charges
                                request.session['discountamount']=discount
                                request.session['coupon']=coupon
                                request.session['couponpercent']=c.discount
                                request.session['actualamount']=total
                                return JsonResponse({"message":True,"total":float(totall),"percent":c.discount,"discount":"{:.2f}".format(discount)})
                            # else:
                            #     return JsonResponse({"message":False})
                        else:
                          
                            return JsonResponse({"message":False})
                    else:
                        
                        return JsonResponse({"message":False})
                else:
                   
                    return JsonResponse({"message":False})
            except Exception as e:
                return JsonResponse({"message":False})
        if request.POST.get("action")=="prescription":
            coupon=request.POST.get("coupon")
            total=request.POST.get("total")
            uni=request.POST.get("uni")
            citi=request.session.get("tempcity")
            try:
                c=coupons.objects.get(couponcode=coupon,status="active")
                couponcount=couponredeem.objects.select_related("user").filter(coupon=coupon).count()
                presc=Prescriptionbook1.objects.prefetch_related("test_name").get(bookingid=uni)
                if presc.coupon==None:
                    if datetime.now(timezone.utc)>c.startdate:
                        if datetime.now(timezone.utc)<c.enddate:
                            if c.cityy.filter(cityname=citi).exists():
                                # if c.limit!=0 or c.limit>0:
                                try:
                                    if couponcount<c.limit:
                                        c.discount
                                        discount=(float(total)*(int(c.discount)/100))
                                        totall=(float(total)-int(discount))+shipping_charges
                                        request.session['discountamount']=discount
                                        request.session['coupon']=coupon
                                        request.session['couponpercent']=c.discount
                                        request.session['actualamount']=total
                                        return JsonResponse({"message":True,"total":float(totall),"percent":c.discount,"discount":"{:.2f}".format(discount)})
                                    else:
                                        return JsonResponse({"message":False})
                                except:
                                    c.discount
                                    discount=(float(total)*(int(c.discount)/100))
                                    totall=(float(total)-int(discount))+shipping_charges
                                    request.session['discountamount']=discount
                                    request.session['coupon']=coupon
                                    request.session['couponpercent']=c.discount
                                    request.session['actualamount']=total
                                    return JsonResponse({"message":True,"total":float(totall),"percent":c.discount,"discount":"{:.2f}".format(discount)})
                                # else:
                                #     return JsonResponse({"message":False})
                            else:
                                return JsonResponse({"message":False})
                        else:
                            return JsonResponse({"message":False})
                    else:
                        return JsonResponse({"message":False})
                else:
                    return JsonResponse({"message":"exists"})
            except Exception as e:
                print("---------",e)
                return JsonResponse({"message":False})
    
def razorpayclose(request):
    if request.method=="POST":
        paymentid=request.POST["paymentid"]
        a=book_history.objects.select_related("user").filter(payment_id=paymentid)
        b=invoicee.objects.filter(order_id=paymentid)
        c=couponredeem.objects.select_related("user").filter(order_id=paymentid)
        d=book_history.objects.select_related("user").get(payment_id=paymentid)
        tes=testbook.objects.select_related("user").filter(bookingid=d.bookingid)
        pres=Prescriptionbook1.objects.prefetch_related("user").filter(bookingid=d.bookingid)
        gos=gosamplify.objects.filter(orderref=d.bookingid)
        crelio=creliohealthdata.objects.filter(spanbookingid=d.bookingid)
        tes.delete()
        pres.delete()
        b.delete()
        a.delete()
        c.delete()
        crelio.delete()
        for i in gos:
            url = f"https://mtqn0qowxc.execute-api.us-east-1.amazonaws.com/delete-customer-visit/{i.taskid}"
            payload={}
            headers = {
              'api-key': gosamplify_apikey,
              'customer-code': customer_code,
            'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            # print("------------",response.text)
            # print("------------",response.status_code)
        gos.delete()
        return JsonResponse({"message":True})
    
def contactuss(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        subject=request.POST["subject"]
        message=request.POST["message"]
        contactus.objects.create(fullname=name,email=email,phone=phone,subject=subject,message=message).save()
        message1 = f"Hi {name},\nThank you for contacting us.\nWe have received your query, our internal team will get in touch with you in no time.\nWe welcome you to checkout our top packages in your region till we get back you.\nThank You,\nDIAGNOSTICA SPAN"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = message
        subject = "Contact us Enquiry | DIAGNOSTICA SPAN"
        customerEmailThread(subject, message1, recipient_list).start()
        messages.success(request,"Your response submitted successfully")
        return redirect('contactus')
        # return render(request,"contactus.html")
    return render(request,"contactus.html") 
def healthcheckupadd(request):
    cityy=request.session.get("city")
    deviceCookie = request.COOKIES['device']
    RES = {}
    if request.method=="POST":
        if request.POST.get("action") == "healthcheckup":
            slug=request.POST["ids"]
            labtest=healthcheckuppackages.objects.prefetch_related("test_name").get(id=slug)
            if cityy==Bangalore:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.dBanglore_price
                )
                res = {"message":created,"test":labtest.package_title}
                RES = res
            
            elif cityy == Mumbai:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.dMumbai_price
                )
                res = {"message":created}
                RES = res

            elif cityy == Bhophal:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.dbhopal_price,
                )
                res = {"message":created}
                RES = res

            elif cityy == Nanded:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.dnanded_price,
                )
                res = {"message":created}
                
                RES = res
            elif cityy == Pune:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.dpune_price,
                )
                res = {"message":created}
                RES = res
            elif cityy == Barshi:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.dbarshi_price,
                )
                res = {"message":created}
                RES = res
            elif cityy == Aurangabad:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.daurangabad_price,
                )
                res = {"message":created}
                RES = res
            
        if request.POST.get("action") == "healthpackage":
            slug=request.POST["ids"]
            package=healthpackages.objects.get(id=slug)
            
            if cityy==Bangalore:
                obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                packages = package,
                user = request.user if not request.user.is_anonymous else None,
                price=package.Banglore_price,
                )
                res = {"message":created,"pack":package.package_name}
                RES = res

            elif cityy == Mumbai:
                obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                packages = package,
                user = request.user if not request.user.is_anonymous else None,
                price=package.Mumbai_price,
                )
                res = {"message":created}
                RES = res

            elif cityy == Bhophal:
                obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                packages = package,
                user = request.user if not request.user.is_anonymous else None,
                price=package.bhopal_price,
                )
                res = {"message":created}
                RES = res

            elif cityy == Nanded:
                obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                packages = package,
                user = request.user if not request.user.is_anonymous else None,
                price=package.nanded_price,
                )
                res = {"message":created}
                RES = res
                
            elif cityy == Pune:
                obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                packages = package,
                user = request.user if not request.user.is_anonymous else None,
                price=package.pune_price,
                )
                res = {"message":created}
                RES = res

            elif cityy == Barshi:
                obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                packages = package,
                user = request.user if not request.user.is_anonymous else None,
                price=package.barshi_price,
                )
                res = {"message":created}
                RES = res

            elif cityy == Aurangabad:
                obj, created = cart.objects.get_or_create(
                device = deviceCookie,
                packages = package,
                user = request.user if not request.user.is_anonymous else None,
                price=package.aurangabad_price,
                )
                res = {"message":created}
                RES = res
        if request.user.is_anonymous:
            request.session['cart_count']= cart.objects.filter(device = deviceCookie).count()
        else:
            request.session['cart_count']= cart.objects.filter(user = request.user).count()

        return JsonResponse(RES)

def faqs(request):
    faqss=faq.objects.all()
    faqscount=faq.objects.all().count()
    return render(request,"faq.html",{"faqs":faqss,"faqscount":faqscount})

def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required(login_url="/login/")
def invoice(request,orderid):
    order=book_history.objects.select_related("user").get(payment_id=orderid)
    payments=payment.objects.select_related("user").get(transid=orderid)
    try:
        testbooking=Prescriptionbook1.objects.prefetch_related("test_name").get(bookingid=order.uni)
    except:
        testbooking=testbook.objects.select_related("user").get(bookingid=order.uni)
    invoic=invoicee.objects.filter(order_id=orderid)
    amount=payments.amount
    # couponamount=num2words(int(float(couponamount)), lang = 'en_IN')
    # a=couponamount.replace(",","")
    # amount=num2words(int(float(amount)), lang = 'en_IN')
    # b=amount.replace(",","")
    amount1=num2words(int(float(amount)), lang = 'en_IN')
    c=amount1.replace(",","")
    try:
        coupoonn=couponredeem.objects.select_related("user").get(order_id=orderid)
        couponamount=coupoonn.actualamount
        couponamount=num2words(int(float(couponamount)), lang = 'en_IN')
        a=couponamount.replace(",","")
        amount=num2words(int(float(amount)), lang = 'en_IN')
        b=amount.replace(",","")
        context_dict={
        
        "order":order,
        "payments":payments,
        "testbooking":testbooking,
        "tests":invoic,
        "coupon":coupoonn,
        "couponamount":a,
        "amount":b
            }
        
    except:
        # coupoonn=couponredeem.objects.get(order_id=orderid)
        context_dict={
        "order":order,
        "payments":payments,
        "testbooking":testbooking,
        "tests":invoic,
        # "couponamount":num2words(int(couponamount), to = 'ordinal'),
        "amount":c
            }
    template_name='invoice2.html'
    from django.core.files import File
    pdf = html_to_pdf(template_name,context_dict)
    receipt_file = BytesIO(pdf.content)
    a=File(receipt_file, "invoice2.pdf")
    filee = invoicee.objects.filter(order_id=orderid).update(file=File(receipt_file, "invoice/invoice2.pdf"))
    return FileResponse(pdf,as_attachment=True,filename="invoice2.pdf",content_type='application/pdf') 

from django.contrib.auth.mixins import LoginRequiredMixin
class BookingHistoryPay(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request,*args, **kwargs):
        # medics=medications.objects.filter(user=request.user)
        medics=medications.objects.select_related("user").filter(user=request.user).order_by("-created")
        his = []
        cit=city.objects.filter(active=True)
        bookhistories=book_history.objects.select_related("user").filter(user=request.user,booking_type__in=["Prescription","Selected Test/Packages"]).order_by('-created')
        # bookhistories=book_history.objects.exclude(user=request.user,booking_type="Aggregator").order_by('-created')
        payments=payment.objects.select_related("user").filter(user=request.user).order_by('-date')
        for i in bookhistories:
            try:
                # try:
                testbooking=Prescriptionbook1.objects.prefetch_related("test_name").get(bookingid=i.uni)
                # except:
                #     pass
                hi = {}
                hi["id"] = i.id
                hi["created"] = i.created
                hi["patient_info"] = i.patient_info
                hi["testbooking_id"] = i.testbooking_id
                hi["uni"]=i.uni
                hi["bookingid"] = i.bookingid
                hi["patient_info"] = i.patient_info
                hi["booking_type"] = i.booking_type
                hi["bookingdetails"] = i.bookingdetails
                hi["paymentmethod"] = testbooking.paymentmethod
                try:
                    hi['prescription'] = testbooking.prescription_file
                except:
                    hi['prescription'] = None
                hi['payment_status'] = i.payment_status
                try:
                    hi['report'] = testbooking.report
                except:
                    hi['report'] = None
                hi['amount'] = i.amount
                his.append(hi)
            except:
                # try:
                testbooking=testbook.objects.select_related("user").get(bookingid=i.uni)
                # except:
                #     pass
                hi = {}
                hi["id"] = i.id
                hi["created"] = i.created
                hi["patient_info"] = i.patient_info
                hi["testbooking_id"] = i.testbooking_id
                hi["uni"]=i.uni
                hi["bookingid"] = i.bookingid
                hi["patient_info"] = i.patient_info
                hi["booking_type"] = i.booking_type
                hi["bookingdetails"] = i.bookingdetails
                hi["paymentmethod"] = None
                # hi['prescription'] = testbooking.prescription_file
                hi['payment_status'] = i.payment_status
                try:
                    hi['report'] = testbooking.report
                except:
                    hi['report'] = None
                hi['amount'] = i.amount
                his.append(hi)
        context={
            "medicscount":medics.count(),
            "medics":medics,
            "city":cit,
            "bookhistories":his,
            "bookinghistorylength":len(his),
            "paymentcount":payments.count(),
            "payments":payments,
            # "testbooking":testbooking,
        }
        return render(request,"booking-history.html",context)
    
    def post(self, request, *args, **kwargs):
        coup=request.session.get("coupon")
        couponper=request.session.get("couponpercent")
        if couponper!=None:
            perc=str(couponper)
        else:
            perc="0"
        if coup!=None:
            coupo=str(coup)
        else:
            coupo="-"
        if request.POST.get("action") == "retreive_data":
            id=request.POST.get('id')
            date=request.POST["date"]
            timeslot=request.POST.get("timeslot")
            citid=request.POST["city"]
            address=request.POST["address"]
            pincode=request.POST["pincode"]
            paymentmethod=request.POST["paymentmethod"]
            coupon=request.POST.get("coupon")
            amount=request.POST["amount"]
            landmark=request.POST.get("landmark")
            dob=request.POST.get("dob")
            price=float(amount.split("₹ ")[1])
            cc=citid.split(',')
            presc=Prescriptionbook1.objects.get(bookingid=id)
            cc=citid.split(',')
            url = "https://mtqn0qowxc.execute-api.us-east-1.amazonaws.com/create-customer-order"
            if presc.gender=="m":
                genderr="Male"
            elif presc.gender=="f":
                genderr="Female"
            else:
                genderr="Other"
            tes=[]
            testli=[]
            for i in presc.test_name.all():
                dic={}
                dicc={}
                a=dic["tests_code"]=i.testcode
                dicc["testCode"]=i.testcode
                testli.append(dicc)
                tes.append(dic)
            payload = json.dumps({
                  "order_ref_id": id,
                  "lab_code": "DIASPAN",
                  "patient_address": address,
                  "patient_pincode": pincode,
                  "patient_phone": request.user.phone_no,
                  "altphone": request.user.phone_no,
                  "date": date,
                  "slot": timeslot,
                  "patient_email": request.user.email,
                  "patient_landmark": landmark,
                  "payment_type": "Prepaid",
                  "total_amount": price,
                  "discount_type": "Percentage",
                  "discount_value": perc,
                  "payment_amount":price,
                  "advance_paid": price,
                  "payment_to_collect": "0",
                  "is_test": 1,
                  "patients": [
                    {
                      "patient_ref_id": "null",
                      "first_name": presc.firstname,
                      "last_name": presc.lastname,
                      "gender": genderr,
                      "age": presc.age,
                      "remark": "MEDITEST",
                      "tests":tes
                    }
                  ]
                })
            headers = {
                  'api-key': gosamplify_apikey,
                  'customer-code': customer_code,
                  'Content-Type': 'application/json'
                }
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(json.loads(response.text))
            res=json.loads(response.text)
            # print("----",response.status_code)
            if response.status_code==201:
                gosamporderid=res["data"][0]["order_number"]
                gosamtaskid=res["data"][0]["task_id"]
                citi=city.objects.get(id=int(cc[0]))
                tokencity=request.session.get("tempcity")
                appointres=appointment(testli,presc.firstname,presc.lastname,presc.age,genderr,gosamporderid,citi.cityname,dob,tokencity)
                # print("------------",json.loads(appointres))
                appointress=json.loads(appointres)
                if appointress["code"]==200:
                    creliohealthdata.objects.create(organisationid=appointress["organisationid"],billid=appointress["billid"],spanbookingid=id,gosamplifyorderid=gosamporderid,gosamplifytaskid=gosamtaskid,labtoken=appointress["labtoken"]).save()
                    goordernumber=res["data"][0]["order_number"]
                    taskid=res["data"][0]["task_id"]
                    orderref=res["data"][0]["order_ref_number"]
                    slotdate=res["data"][0]["slot_date"]
                    slottime=res["data"][0]["slot_time"]
                    amountt=res["data"][0]["amount_to_collect"]
                    patientname=res["data"][0]["main_patient_name"]
                    email=res["data"][0]["patient_email"]
                    phone=res["data"][0]["patient_phone"]
                    addres=res["data"][0]["patient_address"]
                    pincodee=res["data"][0]["patient_pincode"]
                    status=res["data"][0]["status"]
                    payment_type=res["data"][0]["payment_type"]
                    price_=res["data"][0]["amount_to_collect"]
                    gosamplify.objects.create(
                        goordernumber=goordernumber,taskid=taskid,orderref=orderref,couponcode=coupo,paymenttype=payment_type,price=price,couponval=perc,slotdate=slotdate,slottime=slottime,amountt=amountt,patientname=patientname,email=email,phone=phone,address=addres,pincode=pincodee,status=status
                    ).save()
                    try:
                        coup=coupons.objects.get(couponcode=coupon)
                        citi=city.objects.get(id=int(cc[0]))
                        Prescriptionbook1.objects.prefetch_related("test_name").filter(bookingid=id).update(date=date,timeslot=timeslot,location=citi.cityname,address=address,pincode=pincode,paymentmethod=paymentmethod,coupon=coup,price=price,landmark=landmark)
                        mod = book_history.objects.select_related("user").get(uni=id)
                        mod.amount=price
                        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                        tot_amt = float(mod.amount) * 100
                        razorpay_order = client.order.create(
                            {"amount": tot_amt, "currency": "INR", "payment_capture": "1"}
                        )
                        mod.payment_id = razorpay_order['id']
                        mod.save()
                        coupon=request.session.get("coupon")
                        discountamount=request.session.get("discountamount")
                        couponpercent=request.session.get("couponpercent")
                        actualamount= request.session.get("actualamount")
                        if coupon!= None and discountamount!=None and couponpercent!=None and actualamount!=None:
                             couponredeem.objects.create(user=request.user,booking_id=id,order_id=history.payment_id,coupon=request.session.get("coupon"),discountpercen=request.session.get("couponpercent"),discountamount=request.session.get("discountamount"),actualamount=request.session.get('actualamount')).save()
                        if coupon!=None:
                            del request.session['coupon']
                        if discountamount!=None:
                            del request.session['discountamount']
                        if couponpercent!=None:
                            del request.session['couponpercent']
                        if actualamount!=None:
                            del request.session['actualamount']

                        callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,tot_amt//100))
                        # callback_url = 'https://spandiagno.com/paymenthandler/{}/{}/'.format(request.user.email,tot_amt//100) 
                        to_return = {
                            "razorKey":settings.RAZOR_KEY_ID,
                            "valid":True,
                            "amount":tot_amt,
                            "order_id":razorpay_order['id'],
                            "callbackUrl":callback_url,
                        }
                    except:
                        citi=city.objects.get(id=int(cc[0]))
                        Prescriptionbook1.objects.prefetch_related("test_name").filter(bookingid=id).update(date=date,timeslot=timeslot,location=citi.cityname,address=address,pincode=pincode,paymentmethod=paymentmethod,landmark=landmark)
                        mod = book_history.objects.select_related("user").get(uni=id)

                        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                        tot_amt = float(mod.amount) * 100
                        razorpay_order = client.order.create(
                            {"amount": tot_amt, "currency": "INR", "payment_capture": "1"}
                        )
                        mod.payment_id = razorpay_order['id']
                        mod.save()
                        scheme=request.scheme
                        urll=request.get_host()
                        # callback_url=scheme+"://"+urll+'/paymenthandler/{}/{}/'.format(request.user.email,tot_amt//100)
                        callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,tot_amt//100))
                        # callback_url = 'https://spandiagno.com/paymenthandler/{}/{}/'.format(request.user.email,tot_amt//100) 
                        to_return = {
                            "razorKey":settings.RAZOR_KEY_ID,
                            "valid":True,
                            "amount":tot_amt,
                            "order_id":razorpay_order['id'],
                            "callbackUrl":callback_url,
                        }
                    try:
                        items=Prescriptionbook1.objects.get(bookingid=id)
                        for item in items.test_name.all():
                            cityy=request.session.get("city")
                            if cityy==Bangalore:
                                invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.Banglore_price)
                            elif cityy==Mumbai:
                                invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.Mumbai_price)
                            elif cityy==Bhophal:
                                invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.bhopal_price)
                            elif cityy==Nanded:
                                invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.nanded_price)
                            elif cityy==Pune:
                                invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.pune_price)
                            elif cityy==Barshi:
                                invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.barshi_price)  
                            elif cityy==Aurangabad:
                                invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.aurangabad_price)
                    except:
                        items=testbook.objects.get(bookingid=id)
                    # for item in items.test_name.all():
                    #     cityy=request.session.get("city")
                    #     if cityy==Bangalore:
                    #         invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.Banglore_price)
                    #     elif cityy==Mumbai:
                    #         invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.Mumbai_price)
                    #     elif cityy==Bhophal:
                    #         invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.bhopal_price)
                    #     elif cityy==Nanded:
                    #         invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.nanded_price)
                    #     elif cityy==Pune:
                    #         invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.pune_price)
                    #     elif cityy==Barshi:
                    #         invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.barshi_price)  
                    #     elif cityy==Aurangabad:
                    #         invoicee.objects.create(user=request.user,order_id=razorpay_order['id'],items=item,price=item.aurangabad_price)   
                else:
                    to_return = {"valid":False}
            elif response.status_code==401:
                subject=f"401 Unauthorised for Go Samplify"
                message=f"Hi There,\nGo Samplify Order Creating API is Getting Unauthorised Error,Error Code :401\nPlease Lookinto it"
                AdminEmailThread(subject, message, reachus).start()
                to_return = {"valid":False}
            else:
                to_return = {"valid":False}
        if request.POST.get("action") == "payment_canceled":
            mod = book_history.objects.select_related("user").get(payment_id=request.POST.get('order_id'))
            gos=gosamplify.objects.filter(orderref=mod.bookingid)
            mod.payment_id = None
            mod.payment_status = False
            mod.save()
            for i in gos:
                url = f"https://mtqn0qowxc.execute-api.us-east-1.amazonaws.com/delete-customer-visit/{i.taskid}"
                payload={}
                headers = {
                  'api-key': gosamplify_apikey,
                  'customer-code': customer_code,
                    'Content-Type': 'application/json'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                # print("------------",response.text)
                # print("------------",response.status_code)
            gos.delete()
            to_return = {"valid":True}
        if request.POST.get("action") == "COD":
            id=request.POST.get("id")
            date=request.POST.get("date")
            timeslot=request.POST.get("timeslot")
            citid=request.POST.get("city")
            address=request.POST.get("address")
            pincode=request.POST.get("pincode")
            paymentmethod=request.POST.get("paymentmethod")
            coupon=request.POST.get("coupon")
            amount=request.POST.get("amount")
            landmark=request.POST.get("landmark")
            dob=request.POST.get("dob")
            price=float(amount.split("₹ ")[1])
            presc=Prescriptionbook1.objects.get(bookingid=id)
            cc=citid.split(',')
            url = "https://mtqn0qowxc.execute-api.us-east-1.amazonaws.com/create-customer-order"
            if presc.gender=="m":
                genderr="Male"
            elif presc.gender=="f":
                genderr="Female"
            else:
                genderr="Other"
            tes=[]
            testli=[]
            for i in presc.test_name.all():
                dic={}
                dicc={}
                a=dic["tests_code"]=i.testcode
                dicc["testCode"]=i.testcode
                testli.append(dicc)
                tes.append(dic)
            payload = json.dumps({
                  "order_ref_id": id,
                  "lab_code": "DIASPAN",
                  "patient_address": address,
                  "patient_pincode": pincode,
                  "patient_phone": request.user.phone_no,
                  "altphone": request.user.phone_no,
                  "date": date,
                  "slot": timeslot,
                  "patient_email": request.user.email,
                  "patient_landmark": landmark,
                  "payment_type": "Postpaid",
                  "total_amount": price,
                  "discount_type": "Percentage",
                  "discount_value": perc,
                  "payment_amount":price,
                  "advance_paid": "0",
                  "payment_to_collect": price,
                  "is_test": 1,
                  "patients": [
                    {
                      "patient_ref_id": "null",
                      "first_name": presc.firstname,
                      "last_name": presc.lastname,
                      "gender": genderr,
                      "age": presc.age,
                      "remark": "MEDITEST",
                      "tests":tes
                    }
                  ]
                })
            headers = {
                  'api-key': gosamplify_apikey,
                  'customer-code': customer_code,
                  'Content-Type': 'application/json'
                }
            response = requests.request("POST", url, headers=headers, data=payload)
            # print(json.loads(response.text))
            res=json.loads(response.text)
            # print("----",response.status_code)
            if response.status_code==201:
                gosamporderid=res["data"][0]["order_number"]
                gosamtaskid=res["data"][0]["task_id"]
                citi=city.objects.get(id=int(cc[0]))
                tokencity=request.session.get("tempcity")
                appointres=appointment(testli,presc.firstname,presc.lastname,presc.age,genderr,gosamporderid,citi.cityname,dob,tokencity)
                # print("------------",json.loads(appointres))
                appointress=json.loads(appointres)
                if appointress["code"]==200:
                    creliohealthdata.objects.create(organisationid=appointress["organisationid"],billid=appointress["billid"],spanbookingid=id,gosamplifyorderid=gosamporderid,gosamplifytaskid=gosamtaskid,labtoken=appointress["labtoken"]).save()
                    goordernumber=res["data"][0]["order_number"]
                    taskid=res["data"][0]["task_id"]
                    orderref=res["data"][0]["order_ref_number"]
                    slotdate=res["data"][0]["slot_date"]
                    slottime=res["data"][0]["slot_time"]
                    amountt=res["data"][0]["amount_to_collect"]
                    patientname=res["data"][0]["main_patient_name"]
                    email=res["data"][0]["patient_email"]
                    phone=res["data"][0]["patient_phone"]
                    addres=res["data"][0]["patient_address"]
                    pincodee=res["data"][0]["patient_pincode"]
                    status=res["data"][0]["status"]
                    payment_type=res["data"][0]["payment_type"]
                    price_=res["data"][0]["amount_to_collect"]
                    gosamplify.objects.create(
                        goordernumber=goordernumber,taskid=taskid,orderref=orderref,couponcode=coupo,paymenttype=payment_type,price=price_,couponval=perc,slotdate=slotdate,slottime=slottime,amountt=amountt,patientname=patientname,email=email,phone=phone,address=addres,pincode=pincodee,status=status
                    ).save()
                    try:
                        a=coupons.objects.get(couponcode=coupon)
                        citi=city.objects.get(id=int(cc[0]))
                        Prescriptionbook1.objects.prefetch_related("test_name").filter(bookingid=id).update(date=date,timeslot=timeslot,location=citi.cityname,address=address,pincode=pincode,paymentmethod=paymentmethod,coupon=a,price=price,landmark=landmark)
                        book_history.objects.select_related("user").filter(uni=id).update(amount=price)
                        history=book_history.objects.select_related("user").get(uni=id)
                        coupon=request.session.get("coupon")
                        discountamount=request.session.get("discountamount")
                        couponpercent=request.session.get("couponpercent")
                        actualamount= request.session.get("actualamount")
                        # print("----",coupon,discountamount,couponpercent,actualamount)
                        if coupon!= None and discountamount!=None and couponpercent!=None and actualamount!=None:
                             couponredeem.objects.create(user=request.user,booking_id=id,order_id=history.payment_id,coupon=request.session.get("coupon"),discountpercen=request.session.get("couponpercent"),discountamount=request.session.get("discountamount"),actualamount=request.session.get('actualamount')).save()
                        if coupon!=None:
                            del request.session['coupon']
                        if discountamount!=None:
                            del request.session['discountamount']
                        if couponpercent!=None:
                            del request.session['couponpercent']
                        if actualamount!=None:
                            del request.session['actualamount']
                        email_from = settings.EMAIL_HOST_USER
                        mes=f"Cash On Collection Booking for Booking ID:{id}\nPlease Checkit"
                        subject=f"Cash On Collection | DIAGNOSTICA SPAN | Booking Id:{id}"
                        mess=f"Hi {request.user.first_name}\nYou Have Selected Cash On Collection for Booking Id: {id}\nThank You\nDIAGNOSTICA SPAN "

                        customerEmailThread(subject, mess, [request.user.email]).start()
                        AdminEmailThread(subject, mes, reachus).start()
                    except:
                        citi=city.objects.get(id=int(cc[0]))
                        Prescriptionbook1.objects.prefetch_related("test_name").filter(bookingid=id).update(date=date,timeslot=timeslot,location=citi.cityname,address=address,pincode=pincode,paymentmethod=paymentmethod,landmark=landmark)
                        email_from = settings.EMAIL_HOST_USER
                        subject=f"Cash On Collection | DIAGNOSTICA SPAN | Booking Id:{id}"
                        mes=f"Cash On Collection Booking for Booking ID:{id}\nPlease Checkit"
                        mess=f"Hi {request.user.first_name}\nYou Have Selected Cash On Collection for Booking Id: {id}\nThank You\nDIAGNOSTICA SPAN "

                        customerEmailThread(subject, mess, [request.user.email]).start()
                        AdminEmailThread(subject, mes, reachus).start()
                    to_return = {"valid":True}
                else:
                    to_return = {"valid":False}
            elif response.status_code==401:
                subject=f"401 Unauthorised for Go Samplify"
                message=f"Hi There,\nGo Samplify Order Creating API is Getting Unauthorised Error,Error Code :401\nPlease Lookinto it"
                AdminEmailThread(subject, message, reachus).start()
                to_return = {"valid":False}
            else:
                to_return = {"valid":False}
        return HttpResponse(json.dumps(to_return), content_type="application/json")
class HealthSymptoms(View):
    def get(self, request, *args,**kwargs):
        c=request.session.get("city")
        currentSymptom = kwargs['slug']
        currentObj = healthsymptoms.objects.prefetch_related("test_name").get(slug = currentSymptom)
        obj = healthsymptoms.objects.prefetch_related("test_name").exclude(slug = currentSymptom)
        envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
        res = {
            "currentObj":currentObj,
            "others":obj,
            "city":c,
            "envcity":envcity,
        }
        return render(request, "health_symptoms_details.html", res)
    
    def post(self, request, *args,**kwargs):
        RES = {}
        cityy=request.session.get("city")
        deviceCookie = request.COOKIES['device']
        healthSympObj = healthsymptoms.objects.get(id=request.POST.get('ids'))
        if cityy==Bangalore:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            healthsymptoms = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.discounted_price,)
            res = {"message":created,"pack":healthSympObj.name}
            RES = res
        elif cityy == Mumbai:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.discounted_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Bhophal:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.discounted_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Nanded:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.discounted_price,
            )
            res = {"message":created}
            RES = res
            
        elif cityy == Pune:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.discounted_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Barshi:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.discounted_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Aurangabad:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.discounted_price,
            )
            res = {"message":created}
            RES = res
        if request.user.is_anonymous:
            request.session['cart_count']= cart.objects.filter(device = deviceCookie).count()
        else:
            request.session['cart_count']= cart.objects.filter(user = request.user).count()
        # print(RES)
        return JsonResponse(RES)
def privacypolicy(request):
    return render(request,"privacypolicy.html")
def paymentsrefund(request):
    return render(request,"paymentsrefunds.html")
def termsofuse(request):
    return render(request,"termsofuse.html")
def error_404_view(request, exception):
    # return HttpResponse("404 Page not found")
    return render(request,"404.html")
def error_500_view(request):
    # return HttpResponse("404 Page not found")
    return render(request,"500.html")
import csv
import re
def uploadcsv(request):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            print(csv_file)
            if not csv_file.name.endswith('.csv'):
                messages.warning(
                    request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            def decode_utf8(input_iterator):
                for l in input_iterator:
                    yield l.decode('cp1252')
            reader = csv.DictReader(decode_utf8(request.FILES['csv_upload']))
           
            for row in reader:
                print(row)
                n,tests=test.objects.get_or_create(testcode=row.get("TEST CODE"))
                if row.get("STARTER")=="Y":
                    a=healthpackages.objects.get(package_name="STARTER")
                    a.test_name.add(n)
                if row.get("BASIC")=="Y":
                    a=healthpackages.objects.get(package_name="BASIC")
                    a.test_name.add(n)
                if row.get("STANDARD")=="Y":
                    a=healthpackages.objects.get(package_name="STANDARD")
                    a.test_name.add(n)
                if row.get("PRIME")=="Y":
                    a=healthpackages.objects.get(package_name="PRIME")
                    a.test_name.add(n)
                if row.get("PREMIUM")=="Y":
                    a=healthpackages.objects.get(package_name="PREMIUM")
                    a.test_name.add(n)
          
                    # a=healthpackages.objects.get(package_name="SPAN HEALTH PACKAGE -STANDARD")
                    # a.test_name.add(tests)
                    # obj, created = healthpackages.objects.get_or_create(
                    #         testt=row["Tests"],
                    #         testcode=row["test_code"],
                    #         categoryy=categoryy,
                    #         Banglore_price=row.get("Banglore_price") if row.get("Banglore_price") else None,
                    #         Mumbai_price=row.get("Mumbai_price") if row.get("Mumbai_price") else None,
                    #         bhopal_price=row.get("bhopal_price") if row.get("bhopal_price") else None,
                    #         nanded_price=row.get("nanded_price") if row.get("nanded_price") else None,
                    #         pune_price=row.get("pune_price") if row.get("pune_price") else None,
                    #         barshi_price=row.get("barshi_price") if row.get("barshi_price") else None,
                    #         aurangabad_price=row.get("aurangabad_price") if row.get("aurangabad_price") else None,
                    #         description=des)
                # except IndexError:
                #     pass
                # except (IntegrityError):
                #     form = CsvImportForm()
                #     data = {"form": form}
                #     message = messages.warning(
                #         request, 'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
                #     return render(request, "admin/app1/csv_upload.html",)
            # return redirect("csv")
            # url = reverse('admin:index')
            # return HttpResponseRedirect(url)
            res = render(request, "csv.html")
            return res
        return render(request, "csv.html")
def requestcallheader(request):
    if request.method=="POST":
        try:
            firtname=request.POST["firstname"]
            lastname=request.POST["lastname"]
            phone=request.POST["phone"]
            email=request.POST["email"]
            message1=request.POST["message"]
            print(request.POST)
            # try:
            #     t=test.objects.get(id=int(tests))
            # except:
            #     return JsonResponse({"message":"error"})
            requestcall.objects.create(firstname=firtname,lastname=lastname,phone=phone,email=email,message=message1).save()
            message = f'Hi\nYou have Call back request\nFull Name:{firtname} {lastname}\nMobile:{phone}\nEmail:{email}\nMessage:{message1}'
            email_from = settings.EMAIL_HOST_USER
            # recipient_list = ["enquiry@spanhealth.com"]
            message = message
            subject = "Request Call back" 
            # send_mail(
            #             subject,
            #             message,
            #             email_from,
            #             recipient_list,
            #             fail_silently=False,
            #     )
            AdminEmailThread(subject, message, reachus).start()
            return JsonResponse({"message":True})
        except:
            return JsonResponse({"message":"error"})
def lifestyleassessment(request):
    healthsymptom=healthsymptoms.objects.prefetch_related("test_name").all()
    context={
         "healthsymptom":healthsymptom,
    }
    return render(request,"lifestyleassessmentall.html",context)

def lifestyletests(request):
    if request.method=="POST":
        id=request.POST.getlist("pk[]")
        deviceCookie = request.COOKIES.get('device')
        if not request.user.is_anonymous:
            carts = cart.objects.select_related("user").filter(user=request.user)
        else:
            carts = cart.objects.select_related("user").filter(device=deviceCookie)
        test1=[]
        for carrt in carts:
            if str(carrt.items.id) in id:
                test1.append(str(carrt.items.id))
        return JsonResponse({"message":test1})
def medicationsview(request):
    if request.method=="POST":
        try:
            medic=request.POST["medico"]
        except:
            medic="off"
        try:
            morning=request.POST["tab_morning"]
        except:
            morning="off"
        try:
            afternoon=request.POST["tab_afternoon"]
        except:
            afternoon="off"
        try:
            evening=request.POST["tab_evening"]
        except:
            evening="off"
        try:
            night=request.POST["tab_night"]
        except:
            night="off"
        medications.objects.create(user=request.user,medic=medic,morning=True if morning == 'on' else False,afternoon=True if afternoon == 'on' else False,evening=True if evening == 'on' else False,night=True if night == 'on' else False).save()
        return JsonResponse({"message":True})    
def medicationinfo(request):
    if request.method=="POST":
      id=request.POST["pk"]
      medication=medications.objects.select_related("user").get(id=id)
      return JsonResponse({"message":True,"id":medication.id,"medic":medication.medic,"morning":medication.morning,"afternoon":medication.afternoon,"evening":medication.evening,"night":medication.night})  
def medicationdelete(request):
    if request.method=="POST":
        id=request.POST["pk"]
        medications.objects.select_related("user").get(id=id).delete()
        medicocount=medications.objects.select_related("user").all().count()
        return JsonResponse({"message":True,"medicocount":medicocount})  
def medicupdate(request):
    if request.method=="POST":
        id=request.POST["medicid"]
        try:
            medic=request.POST["update_name"]
        except:
            medic="off"
        try:
            morning=request.POST["tabmorningupdate"]
        except:
            morning="off"
        try:
            afternoon=request.POST["tabafternoonupdate"]
        except:
            afternoon="off"
        try:
            evening=request.POST["tabeveningupdate"]
        except:
            evening="off"
        try:
            night=request.POST["tabnightupdate"]
        except:
            night="off"
        medications.objects.select_related("user").filter(id=id).update(user=request.user,medic=medic,morning=True if morning == 'on' else False,afternoon=True if afternoon == 'on' else False,evening=True if evening == 'on' else False,night=True if night == 'on' else False)
        return JsonResponse({"message":True}) 
        # id=request.POST["pk"]
        # medications.objects.filter(pk=some_value).update(field1='some value')   
def franchise(request):
    if request.method=="POST":
        try:
            fullname=request.POST["name"]
            phoneno=request.POST["phone"]
            email=request.POST["email"]
            taluka=request.POST["taluka"]
            district=request.POST["district"]
            state=request.POST["state"]
            address=request.POST["address"]
            message=request.POST["message"]
            franchisee.objects.create(fullname=fullname,phoneno=phoneno,email=email,taluka=taluka,district=district,state=state,address=address,message=message).save()
            messages.success(request,"Submitted Successfully")
            return redirect("franchise")
            # return render (request,"franchisee.html")
        except:
            messages.error(request,"Something went wrong")
            return redirect("franchise")
            # return render (request,"franchisee.html")
    return render (request,"franchisee.html")
def ourcenters(request):
    return render (request,"ourcenters.html")
def career(request):
    designations=careersopenings.objects.all()
    if request.method=="POST":
        fullname=request.POST["name"]
        phoneno=request.POST["phone"]
        email=request.POST["email"]
        cv=request.FILES.get("cv")
        message=request.POST["message"]
        careers.objects.create(fullname=fullname,phoneno=phoneno,email=email,cv=cv,message=message).save()
        messages.success(request,"Submitted Successfully")
        return redirect("career")
        # return render (request,"career.html",{"designations":designations})
    return render (request,"career.html",{"designations":designations})
def sendreport(request,phone,bookingid):
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    request.session['reportbooking']=bookingid
    email=User.objects.get(phone_no=phone)
    message=f"{otp}- is your one time password for Spandiagno Report. Please do not share this OTP with anyone. Spandiagno."
    email_from = settings.EMAIL_HOST_USER
    subject = "DIAGNOSTICA SPAN" 
    recipient_list = [email.email]
    send_mail(
            subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False,
                )
    messages.success(request,"OTP is sent to your Registerd email Please check.")
    return redirect('reportotp')

def reportotp(request):
    if request.method == "POST":
        u_otp1 = request.POST['digit-1']
        u_otp2 = request.POST['digit-2']
        u_otp3 = request.POST['digit-3']
        u_otp4 = request.POST['digit-4']
        otp = request.session.get('otp')
        a=str(u_otp1)+str(u_otp2)+str(u_otp3)+str(u_otp4)
        try:
            if int(a) == otp:
                bookingid=request.session.get('reportbooking')
                try:
                    report=Prescriptionbook1.objects.get(bookingid=bookingid)
                except:
                    report=testbook.objects.get(bookingid=bookingid)
                return FileResponse(report.report,content_type='application/pdf')
            else:
                messages.error(request,'Wrong OTP')
        except Exception as e:
            messages.error(request,"Please Fill all Required Fields")
    return render(request,"reportotp.html")
def readfile(request):
    a=test.objects.filter(Banglore_price__isnull=True)
    file_path1 = os.path.join(settings.STATIC_ROOT)
    file_path= os.path.join(settings.BASE_DIR, 'staticfiles/static')
    # print(file_path)
    f = open("{}/tests.txt".format(file_path), "w")
    f1 = open("{}/tests.txt".format(file_path1), "w")
    for i in a:
        aa="{} {} \n".format(i.id,i.testt)
        f.write(aa)
        f1.write(aa)
    f.close()
    f1.close()
    #open and read the file after the appending:
    # print(f.read())
    # return FileResponse(f,as_attachment=True,filename="tests.txt",content_type='application/text') 
    return render (request,"tests.html")

import requests
def sms(message,mobile):
    try:
        url=f"""https://www.smsidea.co.in/smsstatuswithid.aspx?mobile=9986788880&pass=Malatesh@78&senderid=SPANDS&to={mobile}&msg={message}"""
        # url=f"""https://www.smsidea.co.in/smsstatuswithid.aspx?mobile=9986788880&pass=Malatesh@78&senderid=SPANDS&to={mobile}&msg={message}&peid=1501615380000049113&templateid={templateid}"""
        connection=requests.get(url)
        # b=json.loads(connection.text)
        # print("----",connection.text)
        # res=json.loads(response.text)
        a=connection.text.split(":")
        deliveryurl=f"""https://www.smsidea.co.in/sms/api/msgstatus.aspx?mobile=9986788880&pass=Malatesh@78&msgtempid={a[1].strip()}"""
        deliveryconnection=requests.get(deliveryurl)
        if deliveryconnection.status_code!=200:
            return "Your OTP is not delivered Please try again!"
        else:
            return "Your OTP sent your registered mobile number and Email Id"
    except Exception as e:
        print(e)
        return "Your OTP is not delivered Please try again!"
    
def appointment(testli,firstname,lastname,age,genderr,gosamorder,citname,dob,citytoken):
    try:
        import datetime
        dt = datetime.datetime.now(timezone.utc)
        today = dt.replace(tzinfo=timezone.utc)
        next_2ndday=dt.replace(tzinfo=timezone.utc) + datetime.timedelta(days=4)
        todayy=str(today)
        next_2nddayy=str(next_2ndday)
        # token="c52066e6-3800-11ed-af41-02c92f98bf54"
        # organisationid=370207
        # if citname==Bangalore:
        #     a=creliocitytokens.objects.select_related('city').get(city__cityname=Bangalore)
        #     tokenn=a.token
        #     organisationid=a.orgid
        # elif citname==Mumbai:
        #     a=creliocitytokens.objects.select_related('city').get(city__cityname=Mumbai)
        #     tokenn=a.token
        #     organisationid=a.orgid
        # elif citname==Pune:
        #     a=creliocitytokens.objects.select_related('city').get(city__cityname=Pune)
        #     tokenn=a.token
        #     organisationid=a.orgid
        # else:
            # a=creliocitytokens.objects.select_related('city').get(city__cityname=Mumbai)
            # tokenn=a.token   
            # organisationid=a.orgid
        try:
            a=creliocitytokens.objects.select_related('city').get(city__cityname=citname)
            tokenn=a.token   
            organisationid=a.orgid
        except:
            a=creliocitytokens.objects.select_related('city').get(city__cityname=Bangalore)
            tokenn=a.token   
            organisationid=a.orgid
        # Mumbaitoken="c52066e6-3800-11ed-af41-02c92f98bf54"
        # punetoken="ebf247a8-3800-11ed-b48e-0232dfade036"
        # bangaloretoken="01a5f72a-3fbd-11ed-8614-024670730770"
        # print(type(a))
        # print("------------",a)
        # print("----------",next_2ndday)
        url=f"https://livehealth.solutions/LHRegisterBillAPI/{tokenn}/"
        payload = json.dumps({
        "countryCode": "91",
        "mobile": "",
        "email": "",
        "designation": "",
        "fullName": f"{firstname} {lastname}",
        "firstName": firstname,
        "middleName": "",
        "lastName": lastname,
        "age": age,
        "gender":genderr,
        "area": "",
        "city": "",
        "patientType": "",
        "labPatientId": "",
        "pincode": "",
        "patientId": "",
        "dob": dob,
        "passportNo": "",
        "panNumber": "",
        "aadharNumber": "",
        "insuranceNo": "",
        "nationality": "Indian",
        "ethnicity": "",
        "nationalIdentityNumber": "",
        "workerCode": "",
        "doctorCode": "",
        "areaOfResidence": "",
        "state": "Maharashtra",
        "isAppointmentRequest": 0,
        "startDate":todayy,
        "endDate":next_2nddayy,
        "billDetails": {
          "emergencyFlag": "0",
          "totalAmount": "0",
          "advance": "0",
          "billConcession": "0",
          "additionalAmount": "",
          "billDate": todayy,
          "paymentType": "",
          "referralName": "",
          "otherReferral": "",
          "sampleId": "",
          "orderNumber":gosamorder,
          "referralIdLH": "",
          "organisationName": "",
          "organizationIdLH": organisationid,
          "comments": "New Patient Registration",
          "testList":testli,
          "paymentList": [
            {
              "paymentType": "",
              "paymentAmount": "",
              "issueBank": ""
            }
          ]
          }
          })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print("---------------",response.text)
        # print(payload)
        code=json.loads(response.text)["code"]
        billid=json.loads(response.text)["billId"]
        respp={"code":code,"billid":billid,"organisationid":organisationid,"labtoken":tokenn}
        a=json.dumps(respp)
        return a
    except:
        return ("Something Went Wrong Please Try again")

# import base64
# from django.core.files.base import ContentFile
# def pdfconvert():
#     a="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bWxuczpyZGY9J2h0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMnIHhtbG5zOmlYPSdodHRwOi8vbnMuYWRvYmUuY29tL2lYLzEuMC8nPgo8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0ndXVpZDo0YTIzZDZiNi1lZmE2LTExZTgtMDAwMC05ZmIzZWU2NTk2YjMnIHhtbG5zOnBkZj0naHR0cDovL25zLmFkb2JlLmNvbS9wZGYvMS4zLycgcGRmOlByb2R1Y2VyPSdHUEwgR2hvc3RzY3JpcHQgOS4yMCcvPgo8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0ndXVpZDo0YTIzZDZiNi1lZmE2LTExZTgtMDAwMC05ZmIzZWU2NTk2YjMnIHhtbG5zOnhtcD0naHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyc+PHhtcDpNb2RpZnlEYXRlPjIwMTgtMTEtMjFUMDc6MDM6MzErMDI6MDA8L3htcDpNb2RpZnlEYXRlPgo8eG1wOkNyZWF0ZURhdGU+MjAxOC0xMS0yMVQwNzowMzozMSswMjowMDwveG1wOkNyZWF0ZURhdGU+Cjx4bXA6Q3JlYXRvclRvb2w+VW5rbm93bkFwcGxpY2F0aW9uPC94bXA6Q3JlYXRvclRvb2w+PC9yZGY6RGVzY3JpcHRpb24+CjxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSd1dWlkOjRhMjNkNmI2LWVmYTYtMTFlOC0wMDAwLTlmYjNlZTY1OTZiMycgeG1sbnM6eGFwTU09J2h0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8nIHhhcE1NOkRvY3VtZW50SUQ9J3V1aWQ6NGEyM2Q2YjYtZWZhNi0xMWU4LTAwMDAtOWZiM2VlNjU5NmIzJy8+CjxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSd1dWlkOjRhMjNkNmI2LWVmYTYtMTFlOC0wMDAwLTlmYjNlZTY1OTZiMycgeG1sbnM6ZGM9J2h0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvJyBkYzpmb3JtYXQ9J2FwcGxpY2F0aW9uL3BkZic+PGRjOnRpdGxlPjxyZGY6QWx0PjxyZGY6bGkgeG1s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"
#     a="JVBERi0xLjMKMSAwIG9iago8PAovS2lkcyBbIDQgMCBSIDUgMCBSIDYgMCBSIF0KL1R5cGUgL1BhZ2VzCi9Db3VudCAzCj4+CmVuZG9iagoyIDAgb2JqCjw8Ci9Qcm9kdWNlciAoUHl0aG9uIFBERiBMaWJyYXJ5IFwwNTUgaHR0cFwwNzJcMDU3XDA1N3B5YnJhcnlcMDU2bmV0XDA1N3B5UGRmXDA1NykKPj4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDEgMCBSCj4+CmVuZG9iago0IDAgb2JqCjw8Ci9Db250ZW50cyA3IDAgUgovUGFyZW50IDEgMCBSCi9SZXNvdXJjZXMgPDwKL1hPYmplY3QgPDwKL0Zvcm1Yb2IuMTI3ODVjOWQwNDk2Njk5YmFmNmFmY2RkZWQyMWJjNDIgOCAwIFIKPj4KL0ZvbnQgPDwKL0YyIDkgMCBSCi9GMyAxMCAwIFIKL0YxIDExIDAgUgo+PgovUHJvY1NldCBbIC9UZXh0IC9JbWFnZUMgL0ltYWdlQiAvUERGIC9JbWFnZUkgXQo+PgovVHJhbnMgPDwKPj4KL1JvdGF0ZSAwCi9NZWRpYUJveCBbIDAgMCA1OTUuMjc1NjAgODQxLjg4OTgwIF0KL1R5cGUgL1BhZ2UKPj4KZW5kb2JqCjUgMCBvYmoKPDwKL0NvbnRlbnRzIDEyIDAgUgovUGFyZW50IDEgMCBSCi9SZXNvdXJjZXMgPDwKL1hPYmplY3QgPDwKL0Zvcm1Yb2IuMTI3ODVjOWQwNDk2Njk5YmFmNmFmY2RkZWQyMWJjNDIgOCAwIFIKPj4KL0ZvbnQgPDwKL0YyIDkgMCBSCi9GMyAxMCAwIFIKL0YxIDExIDAgUgo+PgovUHJvY1NldCBbIC9UZXh0IC9JbWFnZUMgL0ltYWdlQiAvUERGIC9JbWFnZUkgXQo+PgovVHJhbnMgPDwKPj4KL1JvdGF0ZSAwCi9NZWRpYUJveCBbIDAgMCA1OTUuMjc1NjAgODQxLjg4OTgwIF0KL1R5cGUgL1BhZ2UKPj4KZW5kb2JqCjYgMCBvYmoKPDwKL0NvbnRlbnRzIDEzIDAgUgovUGFyZW50IDEgMCBSCi9SZXNvdXJjZXMgPDwKL1hPYmplY3QgPDwKL0Zvcm1Yb2IuMTI3ODVjOWQwNDk2Njk5YmFmNmFmY2RkZWQyMWJjNDIgOCAwIFIKPj4KL0ZvbnQgPDwKL0YyIDkgMCBSCi9GMyAxMCAwIFIKL0YxIDExIDAgUgo+PgovUHJvY1NldCBbIC9UZXh0IC9JbWFnZUMgL0ltYWdlQiAvUERGIC9JbWFnZUkgXQo+PgovVHJhbnMgPDwKPj4KL1JvdGF0ZSAwCi9NZWRpYUJveCBbIDAgMCA1OTUuMjc1NjAgODQxLjg4OTgwIF0KL1R5cGUgL1BhZ2UKPj4KZW5kb2JqCjcgMCBvYmoKPDwKL0xlbmd0aCA5OTc3Cj4+CnN0cmVhbQpxCjEgMCAwIDEgMCAwIGNtCkJUCi9GMSAxMiBUZgoxNC40MDAwMCBUTApFVApxCnEKMSAwIDAgMSAyOTcgMjIuODI2NzYgY20KcQoxIDAgMCAxIDEgLTEgY20KcQpxCjUyLjIwMDAwIDAgMCA0NSAwIDIuMDYzMDAgY20KL0Zvcm1Yb2IuMTI3ODVjOWQwNDk2Njk5YmFmNmFmY2RkZWQyMWJjNDIgRG8KUQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDMuODYzMDAgVG0KNDUuNDUwMDAgVEwKNTIuMjAwMDAgMCBUZAovRjEgOSBUZgoxMC44MDAwMCBUTApUKgotNTIuMjAwMDAgMCBUZApFVApRClEKcQpRClEKUQpxCjEgMCAwIDEgMTUgNjU2Ljg4OTgwIGNtCjAgMCAwIHJnCkJUCi9GMSAxMCBUZgoxMiBUTApFVApxCjEgMCAwIDEgMyA4Ny40OTk5OSBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooUGF0aWVudCBOYW1lIFwwNzIgKSBUagovRjIgOSBUZgooTVJcMDU2IEpBTkUgRE9FKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDM5OC41MDAwMCA4Ny40OTk5OSBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooQWdlIFwwNzIgMjQgeWVhcnMgXDA1ME1hbGVcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMgNzAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlZmVycmFsIFwwNzIgRHJcMDU2IFJlZmVycmFsKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDM5OC41MDAwMCA3MCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooUmVnXDA1NiBJRCBcMDcyIElQIFwwNTUgTGFiMTIzNCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzIDUyLjUwMDAwIGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihSZXBvcnQgRGF0ZSBcMDcyIDE0XDA1NzAzXDA1NzIwXDA1NCAxMVwwNzI0NiBBTSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzOTguNTAwMDAgNTIuNTAwMDAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlcG9ydCBJRCBcMDcyIDI2NzM4KSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMgMzUgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFNhbXBsZSBEYXRlIFwwNzIgMTRcMDU3MDNcMDU3MjBcMDU0IDExXDA3MjQ1IEFNKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDM5OC41MDAwMCAzNSBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooU2FtcGxlIElEIFwwNzIgT1AxMjM0NU1SKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMgMTcuNTAwMDAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFByaW50IERhdGUgXDA3MiAxNVwwNTcwNFwwNTcyMFwwNTQgMDNcMDcyMTMgUE0pIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMyAtMCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooU291cmNlIFwwNzIgQWJoaW5hdlwxMzdPcmdcMTM3VGVzdDIpIFRqClQqCkVUClEKUQpxClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNjU1Ljg4OTgwIGNtCnEKMSB3CjEgSgowIDAgMCBSRwpuCjAgMCBtCjU2NSAwIGwKUwpRClEKcQoxIDAgMCAxIDE1IDYzMi4zMDk4MCBjbQpxCjEgMCAwIDEgMSAtMSBjbQpxCjAuOTExMjUgdwowIDAgMCBSRwpuCjE2My4yMjcwMCA3Ljc3ODU0IG0KMzk5Ljc3MzAwIDcuNzc4NTQgbApTCkJUCjEgMCAwIDEgMCA5LjYwMTA0IFRtCjE2My4yMjcwMCAwIFRkCjE0LjU4MDAwIFRMCi9GMiA5LjcyMDAwIFRmCjAgMCAwIHJnCihUSFlST0lEIFBBTkVMXDA1NUlJIFwwNTQgRlJFRSBcMDUwRlQzXDA1NCBGVDRcMDU0IFRTSFwwNTFcMDU0IFNFUlVNKSBUagpUKgotMTYzLjIyNzAwIDAgVGQKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA2MTguODA5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAwIC0wIGNtCnEKMSAwIDAgMSAwIDAgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDcuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YyIDkgVGYKMCAwIDAgcmcKKEludmVzdGlnYXRpb24pIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMjI2IC0wIGNtCnEKMSAwIDAgMSAwIDAgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDcuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YyIDkgVGYKMCAwIDAgcmcKKFZhbHVlXDA1MHNcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMzOSAtMCBjbQpxCjEgMCAwIDEgMCAwIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA3LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMiA5IFRmCjAgMCAwIHJnCihVbml0XDA1MHNcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDYxNy44MDk4MCBjbQpxCjEgdwoxIEoKMCAwIDAgUkcKbgowIDAgbQo1NjUgMCBsClMKUQpRCnEKMSAwIDAgMSAxNSA2MDIuMzA5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAwIC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihGUkVFIFQzKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDIyNiAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooM1wwNTYxIHBnXDA1N21MKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMzOSAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooMlwwNTY1IFwwNTUgM1wwNTY5KSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDU4Ni44MDk4MCBjbQowIDAgMCByZwpCVAovRjEgMTAgVGYKMTIgVEwKRVQKcQoxIDAgMCAxIDAgLTAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKEZSRUUgVDMgXDA1MENNSUFcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDIyNiAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooM1wwNTYyIHBnXDA1N21MKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMzOSAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooMVwwNTY3MSBcMDU1IDNcMDU2NzEpIFRqClQqCkVUClEKUQpxClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNTcxLjMwOTgwIGNtCjAgMCAwIHJnCkJUCi9GMSAxMCBUZgoxMiBUTApFVApxCjEgMCAwIDEgMCAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooRlJFRSBUNCBcMDUwQ01JQVwwNTEpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMjI2IC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCigxXDA1NjIgbmdcMDU3ZEwpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMzM5IC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCigwXDA1NjcwIFwwNTUxXDA1NjQ4KSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDU0Mi4zMDk4MCBjbQowIDAgMCByZwpCVAovRjEgMTAgVGYKMTIgVEwKRVQKcQoxIDAgMCAxIDAgMTMuNTAwMDAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKEZSRUUgVDQgQnkgRUNMSUEpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMjI2IDEzLjUwMDAwIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCigxNCBQbW9sXDA1N0wpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMzM5IC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgMjEuNTM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKENoaWxkcmVuIFwwNzIgMTMgXDA1NSAyNykgVGoKVCoKKEFkdWx0IFwwNzIgMTFcMDU2NSBcMDU1IDIyXDA1NjcpIFRqClQqCkVUClEKUQpxClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNTI2LjgwOTgwIGNtCjAgMCAwIHJnCkJUCi9GMSAxMCBUZgoxMiBUTApFVApxCjEgMCAwIDEgMCAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooRlJFRSBUNFwwNTQgQnkgQ01JQSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAyMjYgLTAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKDEyIG5nXDA1N2RMKSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDUxMS4zMDk4MCBjbQowIDAgMCByZwpCVAovRjEgMTAgVGYKMTIgVEwKRVQKcQoxIDAgMCAxIDAgLTAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFVMVFJBIFRTSCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAyMjYgLTAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKDRcMDU2NSApIFRqCi9GMyA5IFRmCjEzLjUwMDAwIFRMCihtKSBUagovRjEgOSBUZgoxMy41MDAwMCBUTAooSVVcMDU3bWwpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMzM5IC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCigwXDA1NjM1IFwwNTUgNVwwNTY2MCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA0OTUuODA5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAwIC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihVbHRyYSBUU0ggXDA1MENNSUFcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDIyNiAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooNFwwNTYxICkgVGoKL0YzIDkgVGYKMTMuNTAwMDAgVEwKKG0pIFRqCi9GMSA5IFRmCjEzLjUwMDAwIFRMCihJVVwwNTdtTCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzMzkgLTAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKDBcMDU2MzUgXDA1NSA0XDA1Njk0KSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDQ4Mi4zMDk4MCBjbQowIDAgMCByZwpCVAovRjEgMTAgVGYKMTIgVEwKRVQKcQoxIDAgMCAxIDAgLTAgY20KcQoxIDAgMCAxIDAgMCBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgNy4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooICkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA0NjYuODA5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAwIC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihSZW1hcmspIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMjI2IC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihLaW5kbHkgY29ycmVsYXRlIGNsaW5pY2FsbHlcMDU2KSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDM5Ny4zMDk4MCBjbQowIDAgMCByZwpCVAovRjEgMTAgVGYKMTIgVEwKRVQKcQoxIDAgMCAxIDAgNTQgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFVzZSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAyMjYgLTAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKMC44NDM3NSB3CjAuODQzNzUgdwowLjg0Mzc1IHcKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA2Mi4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooRlQ0IGdpdmVzIGNvcnJlY3RlZCB2YWx1ZXMgaW4gcGF0aWVudHMgaW4gd2hvbSB0aGUgdG90YWwgcGVvcGxlIGlzIGFsdGVyZWQgb24gYWNjb3VudCkgVGoKVCoKKG9mIGNoYW5nZXMgaW4gc2VydW0gcHJvdGVpbnMgb3IgaW4gYmluZGluZyBzaWdodHNcMDUwZWdcMDU2IHByZWdlbmVuY3lcMDU0ZHJ1Z1wwNTQgYWx0ZXJlZCBsZXZlbCkgVGoKVCoKKG9mIHNlcnVtIHByb3RlaW5zXDA1MSBNb25pdG9yaW5nIHJlc3RvcmF0aW9uIHRvIG5vcm1hbCByYW5nZSBpcyB0aGUgb25seSBsYWJvcmF0b3J5KSBUagpUKgooY3JpdGVyaW9uIHRvIGVzdGltYXRlIGFwcHJvcHJpYXRlIHJlcGxhY2VtZW50IGRvc2Ugb2YgbGV2b3RoeXJveGluZSBiZWNhdXNlIDZcMDU1OCkgVGoKVCoKKHdlZWtzIGFyZSByZXF1aXJlZCBiZWZvcmUgVFNIIHJlZmxlY3RzIHRoZXNlIGNoYW5nZXNcMDU2KSBUagooICkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSAyNjAuMzA5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAwIDEyMS41MDAwMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooSW50ZXJwcmV0YXRpb24pIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMjI2IC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CjAuODQzNzUgdwowLjg0Mzc1IHcKMC44NDM3NSB3CjAuODQzNzUgdwowLjg0Mzc1IHcKMC44NDM3NSB3CjAuODQzNzUgdwowLjg0Mzc1IHcKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCAxMjkuNTM4MDAgVG0KMTMuNTAwMDAgVEwKL0YyIDkgVGYKMCAwIDAgcmcKKEluY3JlYXNlZCBpbikgVGoKL0YxIDkgVGYKVCoKKEh5cGVydGh5cm9pZGlzbSBIeXBvdGh5cm9pZGlzbSB0cmVhdGVkIHdpdGggdGh5cm94aW5lIEV1dGh5cm9pZCBzaWNrIHN5bmRyb21lKSBUagpUKgooT2NjYXNpb25hbCBwYXRpZW50cyB3aXRoIGh5ZGF0aWRpZm9ybSBtb2xlIG9yIGNob3Jpb2NhcmNpbm9tYSB3aXRoIG1ha2VkIGhDRykgVGoKVCoKKGVsZXZhdGlvbiBtYXkgc2hvdyBpbmNyZWFzZWQgRlQ0XDA1NCBzdXBwcmVzc2VkIFRTSCBhbmQgYmx1bnRlZCBUU0ggcmVzcG9uc2UgdG8pIFRqClQqCihUUkggc3RpbXVsYXRpb25cMDU0IHJldHVybnMgdG8gbm9ybWFsIHdpdGggZWZmZWN0aXZlIHRyZWF0bWVudCBvZiB0cm9waG9ibGFzdGljIGRpc2Vhc2VcMDU0KSBUagpUKgooc2V2ZXJlIGRlaHlhZHJhdGlvblwwNTAgbWF5IGJlIFwwNzYgNlwwNTYwIG5nXDA1N2RsXDA1MSkgVGoKVCoKL0YyIDkgVGYKKERlY3JlYXNlZCBpbikgVGoKL0YxIDkgVGYKVCoKKEh5cG90aHlyb2lkaXNtKSBUagpUKgooSHlwb3RoeXJvaWRpc20gdHJlYXRlZCB3aXRoIHRyaWlvZG90aHlyb25pbmUpIFRqClQqCihFdXRoeXJvaWQgc2ljayBzeW5kcm9tZSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSAyNDQuODA5ODAgY20KcQoxIDAgMCAxIDEgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlbWFya3MpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgMjI5LjMwOTgwIGNtCnEKMSAwIDAgMSAxIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihOb3RlIFwwNzIpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgMjI4LjMwOTgwIGNtCnEKMSB3CjEgSgowIDAgMCBSRwpuCjAgMCBtCjU2NSAwIGwKUwpRClEKcQoxIDAgMCAxIDE1IDIwMi44MDk4MCBjbQpxCjEgMCAwIDEgMSAtMTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDE5LjAzODAwIFRtCjIzNy40OTQ1MCAwIFRkCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihcMDUyXDA1MkVORCBPRiBSRVBPUlRcMDUyXDA1MikgVGoKVCoKLTIzNy40OTQ1MCAwIFRkCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgMTUxLjgwOTgwIGNtCjAgMCAwIHJnCkJUCi9GMSAxMCBUZgoxMiBUTApFVApxCjEgMCAwIDEgMCAtMCBjbQpxCjEgMCAwIDEgMCAtMyBjbQpxCnEKNTIuMjAwMDAgMCAwIDQ1IDAgMyBjbQovRm9ybVhvYi4xMjc4NWM5ZDA0OTY2OTliYWY2YWZjZGRlZDIxYmM0MiBEbwpRCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgMjEuOTAwMDAgVG0KNDUgVEwKNTIuMjAwMDAgMCBUZAovRjEgOSBUZgoxMC44MDAwMCBUTApUKgotNTIuMjAwMDAgMCBUZApFVApRClEKcQpRClEKcQoxIDAgMCAxIDI4Mi41MDAwMCAyNC41MDAwMCBjbQpxCjEgMCAwIDEgMCAtMyBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgMTAuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlZ2lzdGVyZWQgYnkgXDA1NSBBYmhpbmF2KSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDI4Mi41MDAwMCA3IGNtCnEKMSAwIDAgMSAwIC0zIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCAxMC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooUmVwb3J0IGJ5IFwwNTUgTGl2ZWhlYWx0aCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKUQpRClEKcQoxIDAgMCAxIDAgMCBjbQpCVAovRjEgMTIgVGYKMTQuNDAwMDAgVEwKRVQKQlQKL0YxIDkgVGYKMTQuNDAwMDAgVEwKRVQKQlQKMSAwIDAgMSA1MDAgNTAgVG0KKFBhZ2UgMSBvZiAzKSBUagpUKgpFVApRCgplbmRzdHJlYW0KZW5kb2JqCjggMCBvYmoKPDwKL0ZpbHRlciBbIC9BU0NJSTg1RGVjb2RlIC9EQ1REZWNvZGUgXQovTGVuZ3RoIDE0MzAKL0NvbG9yU3BhY2UgL0RldmljZVJHQgovVHlwZSAvWE9iamVjdAovQml0c1BlckNvbXBvbmVudCA4Ci9IZWlnaHQgMTAwCi9XaWR0aCAxMTYKL1N1YnR5cGUgL0ltYWdlCj4+CnN0cmVhbQpzNElBMCEiX2FsOE9gW1whPDwqIyEhKiciczRbTkAhIWljNSM2az47IzZ0Sj8jbV5rSCdGYkhZJE9kbWMnK1ljdClCVSJAKUI5Xz4sVkNHZSt0T3JZKiUzYHAvMi9lODFjLTolM0JdPlc0PiZFSDFCNikvNk5JSyIjbi4xTShfJG9rMSpJVlwxLDpVPzEsOlU/MSw6VT8xLDpVPzEsOlU/MSw6VT8xLDpVPzEsOlU/MSw6VT8xLDpVPzEsOlU/MSw6VT8xLEFtRiEiZko6QSxwXVIhP3FMRiZITXRHIVdVKDwqcmw5QSJUXFcpITxFMyR6ISEhISIhV3JRLyJwWUQ/JDRIbVAhNDxAPCFXYEIqIVgmVC8iVSJyLiEhLktLIVdyRSomSHJkajBnUSFXOy4wXFJFPjEwWk9lRSUqNkYiP0E7VU90WjFMYkJWI21xRmEoYD01PC03OjJqLlBzIkAyYE5mWTZVWEA0N24/M0Q7Y0hhdD0nL1UvQHE5Ll9CNHUhb0YqKVBKR0JlQ1pLN25yNUxQVWVFUCo7LHFRQyF1LFJcSFJRVjVDL2hXTio4MVsnZD9PXEBLMmZfbzBPNmEybEJGZGFRXnJmJThSLWc+ViZPalE1T2VraXFDJm8oMk1IcEBuQFhxWiJKNipydT9EITxFMyUhPEUzJSE8PCoiISEhISIhV3JRLyJwWUQ/JDRIbVAhNDxDPSFXYD8qIjlTYzMiVSJyLiE8UkhGITxOPzgiOWZyJyJxajQhI0BWVGMrdTRdVCdMSXFVWiwkX2sxSypdV0BXS2onKCprYHEtMU1jZykmYWhMLW4tVycyRSpUVTNeWjsoN1JwIUA4bEpcaDxgYEMrPiU7KVNBblBka0MzK0s+RydBMVZIQGdkJktuYkE9TTJJSVtQYS5RJFIkakQ7VVNPYGBWbDZTcFpFcHBHW15XY1ddIylBJ2BRI3M+YWlgJlxlQ0UuJWZcLCE8ajVmPWFrTk0wcW8oMk1IcEBuQFhxWiM3TCRqLU0xIVlHTUghJ15KWD1fPGdCP1MyUElUJCJpdTNnTCdqODxwITBgOGtJJitIY0oiQ1NKTzhEUj1iX1MqbS41cFouM2AzVywzYjxnQFZBXi9BcEYhIyhCNmUlYXAuKVJOT2BwNF5mUis1KGojb2Y1YzM+IUtBSDV1O1tYSms+LC9FIU91TyFNcjRdMnRMbGEyI0VHLC1RYWJXbFcsNnFVbGokQmtTKyg5WiVKWkVWI1g6WydNbmchJ01uZzVtPCpYbEAkVytJKy07PVwlUSFyJDxlWSdUYlxuZCwhL1hYX2YjWDImIU86TDMtJyV1bGo9NThuUFJcJz0nLGdgMzJ0dTVAcGxyb3IzVzg1Y3I5OjgpRUdrbig+JFFWRGk+J0I3WSIoImEtSDpiZ2o6L1daKSpQXi5KLiQoZ1E3XlA+XUojRisoJ2pMSDxKaTEsNTQqcWwpL0RmXSM0KXBEPFZQZlZWPFBIZilYNWpZKlxhOE0sOkIjWGpGLmlDNzAkMm1da2EjUj4wYzdBIyIpIlUiNCxUJD9EPDtXLiYpUyEuJilTIS4mKVMhLl9GQk8sRjJsYCpyQ3EhVTQ9L15XMWQwdSVLTkQoNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwIiQhNzAiJCE3MCIkITcwJWk7ZmB+PgplbmRzdHJlYW0KZW5kb2JqCjkgMCBvYmoKPDwKL0VuY29kaW5nIC9XaW5BbnNpRW5jb2RpbmcKL1R5cGUgL0ZvbnQKL05hbWUgL0YyCi9CYXNlRm9udCAvSGVsdmV0aWNhLUJvbGQKL1N1YnR5cGUgL1R5cGUxCj4+CmVuZG9iagoxMCAwIG9iago8PAovRW5jb2RpbmcgL1N5bWJvbEVuY29kaW5nCi9UeXBlIC9Gb250Ci9OYW1lIC9GMwovQmFzZUZvbnQgL1N5bWJvbAovU3VidHlwZSAvVHlwZTEKPj4KZW5kb2JqCjExIDAgb2JqCjw8Ci9FbmNvZGluZyAvV2luQW5zaUVuY29kaW5nCi9UeXBlIC9Gb250Ci9OYW1lIC9GMQovQmFzZUZvbnQgL0hlbHZldGljYQovU3VidHlwZSAvVHlwZTEKPj4KZW5kb2JqCjEyIDAgb2JqCjw8Ci9MZW5ndGggNDYxOQo+PgpzdHJlYW0KcQoxIDAgMCAxIDAgMCBjbQpCVAovRjEgMTIgVGYKMTQuNDAwMDAgVEwKRVQKcQpxCjEgMCAwIDEgMjk3IDIyLjgyNjc2IGNtCnEKMSAwIDAgMSAxIC0xIGNtCnEKcQo1Mi4yMDAwMCAwIDAgNDUgMCAyLjA2MzAwIGNtCi9Gb3JtWG9iLjEyNzg1YzlkMDQ5NjY5OWJhZjZhZmNkZGVkMjFiYzQyIERvClEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCAzLjg2MzAwIFRtCjQ1LjQ1MDAwIFRMCjUyLjIwMDAwIDAgVGQKL0YxIDkgVGYKMTAuODAwMDAgVEwKVCoKLTUyLjIwMDAwIDAgVGQKRVQKUQpRCnEKUQpRClEKcQoxIDAgMCAxIDE1IDY1Ni44ODk4MCBjbQowIDAgMCByZwpCVAovRjEgMTAgVGYKMTIgVEwKRVQKcQoxIDAgMCAxIDMgODcuNDk5OTkgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFBhdGllbnQgTmFtZSBcMDcyICkgVGoKL0YyIDkgVGYKKE1SXDA1NiBKQU5FIERPRSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzOTguNTAwMDAgODcuNDk5OTkgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKEFnZSBcMDcyIDIzIFlycyAzIE0gXDA1ME1hbGVcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMgNzAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlZmVycmFsIFwwNzIgRHJcMDU2IFJlZmVycmFsKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDM5OC41MDAwMCA3MCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooUmVnXDA1NiBJRCBcMDcyIElQIFwwNTUgTGFiMTIzNCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzIDUyLjUwMDAwIGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihSZXBvcnQgRGF0ZSBcMDcyIDE0XDA1NzAzXDA1NzIwXDA1NCAxMVwwNzI0NiBhXDA1Nm1cMDU2KSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDM5OC41MDAwMCA1Mi41MDAwMCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooUmVwb3J0IElEIFwwNzIgMjY3MzkpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMyAzNSBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooU2FtcGxlIERhdGUgXDA3MiAxNFwwNTcwM1wwNTcyMFwwNTQgMTFcMDcyNDUgYVwwNTZtXDA1NikgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzOTguNTAwMDAgMzUgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFNhbXBsZSBJRCBcMDcyIE9QMTIzNDVNUikgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzIDE3LjUwMDAwIGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihQcmludCBEYXRlIFwwNzIgMTVcMDU3MDRcMDU3MjBcMDU0IDAzXDA3MjEzIHBcMDU2bVwwNTYpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMzk4LjUwMDAwIDE3LjUwMDAwIGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihMb2NhdGlvbiBcMDcyIEJhbmVyKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMgLTAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFNvdXJjZSBcMDcyIEFiaGluYXZcMTM3T3JnXDEzN1Rlc3QyKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDM5OC41MDAwMCAtMCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooSFBFIE5vXDA1NiBcMDcyIEREXDA1NzI2NzM5XDA1NzIwKSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDY1NS44ODk4MCBjbQpxCjEgdwoxIEoKMCAwIDAgUkcKbgowIDAgbQo1NjUgMCBsClMKUQpRCnEKMSAwIDAgMSAxNSA2MzIuMzA5ODAgY20KcQoxIDAgMCAxIDEgLTEgY20KcQowLjkxMTI1IHcKMCAwIDAgUkcKbgoyNjYuMTAzNTAgNy43Nzg1NCBtCjI5Ni44OTY1MCA3Ljc3ODU0IGwKUwpCVAoxIDAgMCAxIDAgOS42MDEwNCBUbQoyNjYuMTAzNTAgMCBUZAoxNC41ODAwMCBUTAovRjIgOS43MjAwMCBUZgowIDAgMCByZwooTGlwYXNlKSBUagpUKgotMjY2LjEwMzUwIDAgVGQKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA2MTguODA5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAwIC0wIGNtCnEKMSAwIDAgMSAwIDAgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDcuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YyIDkgVGYKMCAwIDAgcmcKKEludmVzdGlnYXRpb24pIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMjI2IC0wIGNtCnEKMSAwIDAgMSAwIDAgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDcuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YyIDkgVGYKMCAwIDAgcmcKKFZhbHVlXDA1MHNcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMzOSAtMCBjbQpxCjEgMCAwIDEgMCAwIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA3LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMiA5IFRmCjAgMCAwIHJnCihVbml0XDA1MHNcMDUxKSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDYxNy44MDk4MCBjbQpxCjEgdwoxIEoKMCAwIDAgUkcKbgowIDAgbQo1NjUgMCBsClMKUQpRCnEKMSAwIDAgMSAxNSA2MDIuMzA5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAwIC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihMaXBhc2UpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMjI2IC0wIGNtCnEKMSAwIDAgMSAwIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA4LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCigzMzMgVVwwNTdMKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMzOSAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooNzMgXDA1NSAzOTMpIFRqClQqCkVUClEKUQpxClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNTg2LjgwOTgwIGNtCnEKMSAwIDAgMSAxIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMiA5IFRmCjAgMCAwIHJnCihSZWZlcmVuY2VcMDcyKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDE1IDU3MS4zMDk4MCBjbQpxCjEgMCAwIDEgMSAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooU2llbWVucyBraXQgbGl0ZXJhdHVyZSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA1NTUuODA5ODAgY20KcQoxIDAgMCAxIDEgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlbWFya3MpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNTQwLjMwOTgwIGNtCnEKMSAwIDAgMSAxIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihOb3RlIFwwNzIpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNTM5LjMwOTgwIGNtCnEKMSB3CjEgSgowIDAgMCBSRwpuCjAgMCBtCjU2NSAwIGwKUwpRClEKcQoxIDAgMCAxIDE1IDUxMy44MDk4MCBjbQpxCjEgMCAwIDEgMSAtMTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDE5LjAzODAwIFRtCjIzNy40OTQ1MCAwIFRkCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihcMDUyXDA1MkVORCBPRiBSRVBPUlRcMDUyXDA1MikgVGoKVCoKLTIzNy40OTQ1MCAwIFRkCkVUClEKUQpxClEKUQpRCnEKMSAwIDAgMSAwIDAgY20KQlQKL0YxIDEyIFRmCjE0LjQwMDAwIFRMCkVUCkJUCi9GMSA5IFRmCjE0LjQwMDAwIFRMCkVUCkJUCjEgMCAwIDEgNTAwIDUwIFRtCihQYWdlIDIgb2YgMykgVGoKVCoKRVQKUQoKZW5kc3RyZWFtCmVuZG9iagoxMyAwIG9iago8PAovTGVuZ3RoIDQ2MTkKPj4Kc3RyZWFtCnEKMSAwIDAgMSAwIDAgY20KQlQKL0YxIDEyIFRmCjE0LjQwMDAwIFRMCkVUCnEKcQoxIDAgMCAxIDI5NyAyMi44MjY3NiBjbQpxCjEgMCAwIDEgMSAtMSBjbQpxCnEKNTIuMjAwMDAgMCAwIDQ1IDAgMi4wNjMwMCBjbQovRm9ybVhvYi4xMjc4NWM5ZDA0OTY2OTliYWY2YWZjZGRlZDIxYmM0MiBEbwpRCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgMy44NjMwMCBUbQo0NS40NTAwMCBUTAo1Mi4yMDAwMCAwIFRkCi9GMSA5IFRmCjEwLjgwMDAwIFRMClQqCi01Mi4yMDAwMCAwIFRkCkVUClEKUQpxClEKUQpRCnEKMSAwIDAgMSAxNSA2NTYuODg5ODAgY20KMCAwIDAgcmcKQlQKL0YxIDEwIFRmCjEyIFRMCkVUCnEKMSAwIDAgMSAzIDg3LjQ5OTk5IGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihQYXRpZW50IE5hbWUgXDA3MiApIFRqCi9GMiA5IFRmCihNUlwwNTYgSkFORSBET0UpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMzk4LjUwMDAwIDg3LjQ5OTk5IGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihBZ2UgXDA3MiAyMyBZcnMgMyBNIFwwNTBNYWxlXDA1MSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzIDcwIGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihSZWZlcnJhbCBcMDcyIERyXDA1NiBSZWZlcnJhbCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzOTguNTAwMDAgNzAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlZ1wwNTYgSUQgXDA3MiBJUCBcMDU1IExhYjEyMzQpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMyA1Mi41MDAwMCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooUmVwb3J0IERhdGUgXDA3MiAxNFwwNTcwM1wwNTcyMFwwNTQgMTFcMDcyNDYgYVwwNTZtXDA1NikgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzOTguNTAwMDAgNTIuNTAwMDAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFJlcG9ydCBJRCBcMDcyIDI2NzQwKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDMgMzUgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFNhbXBsZSBEYXRlIFwwNzIgMTRcMDU3MDNcMDU3MjBcMDU0IDExXDA3MjQ1IGFcMDU2bVwwNTYpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMzk4LjUwMDAwIDM1IGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihTYW1wbGUgSUQgXDA3MiBPUDEyMzQ1TVIpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMyAxNy41MDAwMCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooUHJpbnQgRGF0ZSBcMDcyIDE1XDA1NzA0XDA1NzIwXDA1NCAwM1wwNzIxMyBwXDA1Nm1cMDU2KSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDM5OC41MDAwMCAxNy41MDAwMCBjbQpxCjEgMCAwIDEgMyAtMiBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooTG9jYXRpb24gXDA3MiBCYW5lcikgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzIC0wIGNtCnEKMSAwIDAgMSAzIC0yIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihTb3VyY2UgXDA3MiBBYmhpbmF2XDEzN09yZ1wxMzdUZXN0MikgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzOTguNTAwMDAgLTAgY20KcQoxIDAgMCAxIDMgLTIgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKEhQRSBOb1wwNTYgXDA3MiBERFwwNTcyNjc0MFwwNTcyMCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA2NTUuODg5ODAgY20KcQoxIHcKMSBKCjAgMCAwIFJHCm4KMCAwIG0KNTY1IDAgbApTClEKUQpxCjEgMCAwIDEgMTUgNjMyLjMwOTgwIGNtCnEKMSAwIDAgMSAxIC0xIGNtCnEKMC45MTEyNSB3CjAgMCAwIFJHCm4KMjY2LjEwMzUwIDcuNzc4NTQgbQoyOTYuODk2NTAgNy43Nzg1NCBsClMKQlQKMSAwIDAgMSAwIDkuNjAxMDQgVG0KMjY2LjEwMzUwIDAgVGQKMTQuNTgwMDAgVEwKL0YyIDkuNzIwMDAgVGYKMCAwIDAgcmcKKExpcGFzZSkgVGoKVCoKLTI2Ni4xMDM1MCAwIFRkCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNjE4LjgwOTgwIGNtCjAgMCAwIHJnCkJUCi9GMSAxMCBUZgoxMiBUTApFVApxCjEgMCAwIDEgMCAtMCBjbQpxCjEgMCAwIDEgMCAwIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA3LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMiA5IFRmCjAgMCAwIHJnCihJbnZlc3RpZ2F0aW9uKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDIyNiAtMCBjbQpxCjEgMCAwIDEgMCAwIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA3LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMiA5IFRmCjAgMCAwIHJnCihWYWx1ZVwwNTBzXDA1MSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzMzkgLTAgY20KcQoxIDAgMCAxIDAgMCBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgNy4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjIgOSBUZgowIDAgMCByZwooVW5pdFwwNTBzXDA1MSkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA2MTcuODA5ODAgY20KcQoxIHcKMSBKCjAgMCAwIFJHCm4KMCAwIG0KNTY1IDAgbApTClEKUQpxCjEgMCAwIDEgMTUgNjAyLjMwOTgwIGNtCjAgMCAwIHJnCkJUCi9GMSAxMCBUZgoxMiBUTApFVApxCjEgMCAwIDEgMCAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooTGlwYXNlKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDIyNiAtMCBjbQpxCjEgMCAwIDEgMCAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOC4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooMjMyIFVcMDU3TCkgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAzMzkgLTAgY20KcQoxIDAgMCAxIDAgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDguMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKDczIFwwNTUgMzkzKSBUagpUKgpFVApRClEKcQpRClEKcQpRClEKcQoxIDAgMCAxIDE1IDU4Ni44MDk4MCBjbQpxCjEgMCAwIDEgMSAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjIgOSBUZgowIDAgMCByZwooUmVmZXJlbmNlXDA3MikgVGoKVCoKRVQKUQpRCnEKUQpRCnEKMSAwIDAgMSAxNSA1NzEuMzA5ODAgY20KcQoxIDAgMCAxIDEgLTEgY20KcQowLjg0Mzc1IHcKQlQKMSAwIDAgMSAwIDkuMDM4MDAgVG0KMTMuNTAwMDAgVEwKL0YxIDkgVGYKMCAwIDAgcmcKKFNpZW1lbnMga2l0IGxpdGVyYXR1cmUpIFRqClQqCkVUClEKUQpxClEKUQpxCjEgMCAwIDEgMTUgNTU1LjgwOTgwIGNtCnEKMSAwIDAgMSAxIC0xIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCA5LjAzODAwIFRtCjEzLjUwMDAwIFRMCi9GMSA5IFRmCjAgMCAwIHJnCihSZW1hcmtzKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDE1IDU0MC4zMDk4MCBjbQpxCjEgMCAwIDEgMSAtMSBjbQpxCjAuODQzNzUgdwpCVAoxIDAgMCAxIDAgOS4wMzgwMCBUbQoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooTm90ZSBcMDcyKSBUagpUKgpFVApRClEKcQpRClEKcQoxIDAgMCAxIDE1IDUzOS4zMDk4MCBjbQpxCjEgdwoxIEoKMCAwIDAgUkcKbgowIDAgbQo1NjUgMCBsClMKUQpRCnEKMSAwIDAgMSAxNSA1MTMuODA5ODAgY20KcQoxIDAgMCAxIDEgLTExIGNtCnEKMC44NDM3NSB3CkJUCjEgMCAwIDEgMCAxOS4wMzgwMCBUbQoyMzcuNDk0NTAgMCBUZAoxMy41MDAwMCBUTAovRjEgOSBUZgowIDAgMCByZwooXDA1MlwwNTJFTkQgT0YgUkVQT1JUXDA1MlwwNTIpIFRqClQqCi0yMzcuNDk0NTAgMCBUZApFVApRClEKcQpRClEKUQpxCjEgMCAwIDEgMCAwIGNtCkJUCi9GMSAxMiBUZgoxNC40MDAwMCBUTApFVApCVAovRjEgOSBUZgoxNC40MDAwMCBUTApFVApCVAoxIDAgMCAxIDUwMCA1MCBUbQooUGFnZSAzIG9mIDMpIFRqClQqCkVUClEKCmVuZHN0cmVhbQplbmRvYmoKeHJlZgowIDE0CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMDgwIDAwMDAwIG4gCjAwMDAwMDAxODEgMDAwMDAgbiAKMDAwMDAwMDIzMCAwMDAwMCBuIAowMDAwMDAwNTI2IDAwMDAwIG4gCjAwMDAwMDA4MjMgMDAwMDAgbiAKMDAwMDAwMTEyMCAwMDAwMCBuIAowMDAwMDExMTQ5IDAwMDAwIG4gCjAwMDAwMTI3NjYgMDAwMDAgbiAKMDAwMDAxMjg3OCAwMDAwMCBuIAowMDAwMDEyOTgyIDAwMDAwIG4gCjAwMDAwMTMwOTAgMDAwMDAgbiAKMDAwMDAxNzc2MiAwMDAwMCBuIAp0cmFpbGVyCjw8Ci9TaXplIDE0Ci9Sb290IDMgMCBSCi9JbmZvIDIgMCBSCj4+CnN0YXJ0eHJlZgoyMjQzNAolJUVPRgo="
#     datas = ContentFile(base64.b64decode(a), name='repor81.' + "pdf")
#     b=Prescriptionbook1.objects.filter(bookingid="DP22416")
#     for i in b:
#         i.report=File(datas)
#         i.save()
# pdfconvert()    
# def creategosamplifyorder():
#     url = "https://mtqn0qowxc.execute-api.us-east-1.amazonaws.com/create-customer-order"
#     payload = json.dumps({
#       "order_ref_id": "cvbcvbncvbn",
#       "lab_code": "DIASPAN",
#       "patient_address": "A-Wing, Flat No-406, Survodya Anand CHS, Beside Demart, Manpada Road, Dombivli east",
#       "patient_pincode": "412207",
#       "patient_phone": "8112271155",
#       "altphone": "8112271155",
#       "date": "17-09-2022",
#       "slot": "20:00-21:00",
#       "patient_email": "test@gmail.com",
#       "patient_landmark": "",
#       "payment_type": "Postpaid",
#       "total_amount": "399",
#       "discount_type": "Flat",
#       "discount_value": "0",
#       "payment_amount": "399",
#       "advance_paid": "100",
#       "payment_to_collect": "299",
#       "is_test": 1,
#       "patients": [
#         {
#           "patient_ref_id": "null",
#           "first_name": "padam",
#           "last_name": "singh",
#           "gender": "Female",
#           "age": "61",
#           "remark": "MEDITEST",
#           "tests": [
#             {
#               "tests_code": "BI205"
#             }
#           ]
#         }
#       ]
#     })
#     headers = {
#       'api-key': '8517db-ff9614-42c7c9-512743-18780d',
#       'customer-code': 'DIS',
#       'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     # print(response.text)
#     # print(json.loads(response.text))
from .task import send_mail_func,reportsavee
def dummyy(request):
    a=send_mail_func.apply_async()
    b=reportsavee.apply_async()
    # a=Prescriptionbook1.objects.all().values("id")
    # precriptionb = serializers.serialize("json", testbook.objects.all().order_by('-created')[0:10])
    # request.session["dataa"]=precriptionb
    # for i in json.loads(request.session.get("dataa")):
    #     print(i["fields"]["bookingid"])
    return HttpResponse("vsdfvs")