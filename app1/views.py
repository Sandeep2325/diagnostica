import re
# import sweetify
from django.shortcuts import render,redirect
from .forms import UserProfileForm,UserRegistrationForm, forgotpasswordform, prescriptionform, subscriptionform
from django.contrib.auth.hashers import make_password
import random
# from django.contrib.auth.models import User
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

def dashboard(request):
    test=prescription_book.objects.all().count()
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
    for i in  outstand:
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
    request.session["city"]=city
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
            message=f"Hi {f},\nThank You for Choosing DIAGNOSTICA SPAN\nPlease enter this OTP {otp} to verify"
            # message = f'Welcome your otp is {otp} '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            message = message
            subject = "DIGNOSTICA SPAN OTP Confirmation" 
            send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
            )
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

        if int(a) == otp:
            User.objects.create(
                            first_name = firstname,
                            last_name=lastname,
                            email=email_address,
                            phone_no=p_number,
                            password=hash_pwd
            )
            request.session.delete('otp')
            request.session.delete('firstname')
            request.session.delete('lastname')
            request.session.delete('email')
            request.session.delete('password')
            request.session.delete('phone_number')
            messages.success(request,'Registration Successfully Done !!')
            return redirect('/login/')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'otp.html')

def resendotp(request):
    # if request.method=="POST":
    email_address = request.session.get('email')
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    message=f"Hello,\nYour Resend OTP is {otp}\nPlease enter to verify"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_address]
    message = message
    subject = "DIGNOSTICA SPAN" 
    send_mail(
            subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False,
    )
    messages.success(request,"resend otp sent")
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
        message=f"Hi {request.user.first_name},\nThere was a request to Password change\nIf you did not make this request then please ignore this email.\nOtherwise, Please enter the otp {otp}"
        # message = f'Hello,\nWelcome your Change Password OTP is {otp} '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email_address]
        message = message
        subject = "DIGNOSTICA SPAN" 
        send_mail(
                subject,
                message,
                email_from,
                recipient_list,
                fail_silently=False,
            )
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
            request.session['email'] = e
            request.session['password'] = p
            otp = random.randint(1000,9999)
            
            request.session['otp'] = otp
                # message = f'your otp is {otp}'
                # send_otp(p_number,message)
            message = f"Hi Dear Customer,\nThere was a request to Forgot password! Password change\nIf you did not make this request then please ignore this email.\nOtherwise, Please enter the otp {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            message = message
            subject = "DIAGNOSTICA SPAN" 
            send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
            )
            return redirect('/forgotpassword/otp/')
        else:
            messages.error(request,"Email is not registered")
            return render(request,"forgotpassword.html")
    return render(request,"forgotpassword.html")

def changepasswordotp(request):
    print(request.user)
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
        if int(a) == otp:
            data = User.objects.filter(
                            email=request.user.email)
            if data.exists():
                data = User.objects.filter(
                            email=request.user.email).update(password=newpassword)
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
    return render(request,'otpforgot.html')    
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
    send_mail(
            subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False,
    )
    messages.success(request,"resend otp sent")
    return redirect('/forgotpassword/otp/') 

def userinfo(request):
   a= request.user
   return JsonResponse({"message":True,"firstname":a.first_name,"lastname":a.last_name,"contact":a.phone_no,"gender":a.gender,"address":a.address,"age":a.age}) 
@login_required(login_url="/login/")
def profilee(request):
    cityy=city.objects.filter(active=True)
    profile=User.objects.get(email=request.user.email)
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
        try:
            c=city.objects.get(id=int(location))
        except:
            messages.error(request,"Please Update every field")
        if bool(firstname)==False or bool(lastname)==False or bool(phone)==False:
            messages.error(request,"Please Update every field") 
        else:
            a=User.objects.get(email=request.user.email)
            try:
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
                a.save()
                messages.success(request,"Profile updated Successfully")
            except:
                messages.error(request,"Please Update every field")
        # a.age=age
        # a.address=address
        # a.save()
        # messages.success(request,"Profile updated Successfully")
        # profile=User.objects.get(email=request.user.email)
        context1={
            "profile":profile,
            "cityy":cityy,
        }
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
    request.session["city"]="Bangalore"
    deviceCookie = request.COOKIES.get('device')
    c=request.session.get("city")
    envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
    if request.method =="GET":
        cit=city.objects.filter(active=True)
        tests=test.objects.all()
        healthcheckup=healthcheckuppackages.objects.all()[0:4]
        healthpackage=healthpackages.objects.all()
        healthsymptom=healthsymptoms.objects.all()
        healthcareblog=healthcareblogs.objects.all()
        testimonial=testimonials.objects.all()
        if request.user.is_anonymous:
            d = cart.objects.filter(device = deviceCookie)
        else:
            d = cart.objects.filter(user = request.user)
        request.session['cart_count'] = d.count()
        context={
            "healthcheckup":healthcheckup,
            "healthpackage":healthpackage,
            "healthsymptom":healthsymptom,
            "testimonial":testimonial,
            "healthcareblog":healthcareblog,
            "city":cit,
            "currentcity":c,
            "tests":tests,
            "envcity":envcity,
            "blogcount":healthcareblog.count()
        }
        res = render(request,'home.html',context)
        return res

    if request.method=="POST":
        testt=request.POST["selectbookhelp"]
        tes=test.objects.get(id=testt)
        firtname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        message = '{} from {} category from {}'.format(tes.testt,tes.categoryy,c)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ["sandeep.nexevo@gmail.com"]
        message = message
        subject = "You have a test query" 
        send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
            )
        cit=city.objects.all()
        tests=test.objects.all()
        healthcheckup=healthcheckuppackages.objects.all()[0:4]
        healthpackage=healthpackages.objects.all()
        healthsymptom=healthsymptoms.objects.all()
        healthcareblog=healthcareblogs.objects.all()
        testimonial=testimonials.objects.all()
        context={
                "healthcheckup":healthcheckup,
                "healthpackage":healthpackage,
                "healthsymptom":healthsymptom,
                "testimonial":testimonial,
                "healthcareblog":healthcareblog,
                "city":cit,
                "currentcity":c,
                "tests":tests,
                "envcity":envcity,
        }
        messages.success(request,"Submitted Successfully")
        return HttpResponseRedirect(reverse("home"))

def healthcheckupview(request,slug):
    c=request.session.get("city")
    city="Hyderabad"
    data=healthcheckuppackages.objects.filter(slug=slug)[0:4]
    context={
        "data":data,
        "city":city
    }
    return render(request,'dummy.html',context)

def healthcheckupallview(request):
    c=request.session.get("city")
    checkups=healthcheckuppackages.objects.all()
    context={
        "checkups":checkups,
        "currentcity":c
    }
    return render(request,'latestviewall.html',context)
def hpackagess(request):
    packages=healthpackages.objects.all()
    cit=request.session.get("city")
    envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
    context={
        "packages":packages,
        "city":cit,
        "envcity":envcity,
    }
    return render(request,'healthpackages.html',context)

def healthpackageview(request,slug):
        c=request.session.get("city")
        package=healthpackages.objects.get(slug=slug)
        packages=healthpackages.objects.exclude(slug=slug)
        envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
        context={
            "package":package,
            "packages":packages,
            "city":c,
            'envcity':envcity,
        }
        currency = 'INR'
        if c == Bangalore:
            amount=int(package.Banglore_price)
        elif c == Mumbai:
            amount=int(package.Mumbai_price)
        elif c == Bhophal:
            amount=int(package.bhopal_price)
        elif c == Nanded:
            amount=int(package.nanded_price)
        elif c == Pune:
            amount=int(package.pune_price)
        elif c == Barshi:
            amount=int(package.barshi_price)
        elif c == Aurangabad:
            amount=int(package.aurangabad_price)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        try:
            razorpay_order = client.order.create(
                    {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
            )
        except Exception as e:
            razorpay_order = client.order.create(
                    {"amount": 1* 100, "currency": "INR", "payment_capture": "1"}
            )
        request.session['amount']=amount
        razorpay_order_id = razorpay_order['id']
        
        # callback_url = callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        return render(request,'packagedetail.html',context)


def testdetails(request):
    if request.method=="POST":
            id=request.POST["id"]
            a=book_history.objects.get(id=id)
            return JsonResponse({"message":a.bookingdetails})
def prescriptionbreak(request):
    if request.method=="POST":
        city=request.session.get("city")
        id=request.POST["id"]
        print(id)
        a=Prescriptionbook1.objects.get(bookingid=id)
        print(a)
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
        return JsonResponse({"message":strr})
def healthsymptomview(request,slug):
    c=request.session.get("city")
    data=healthsymptoms.objects.filter(slug=slug)
    context={
        "data":data,
        "city":c
    }
    return render(request,'',context)
def healthcareblogsview(request,slug):
    c=request.session.get("city")
    detail=healthcareblogs.objects.get(slug=slug)
    blogs=healthcareblogs.objects.all().order_by("-created")
    category=blogcategory.objects.all()
    context={
        "detail":detail,
        "blogs":blogs, 
        "category":category,
    }
    return render(request,'blogdetail.html',context)
def categoryblog(request,slug):
    detail=healthcareblogs.objects.get(category__slug=slug)
    blogs=healthcareblogs.objects.filter(category__slug=slug).order_by("-created")
    category=blogcategory.objects.all()
    context={
        "detail":detail,
        "blogs":blogs, 
        "category":category,
    }
    return render(request,'blogdetail.html',context)

# def blogdetail(request,slug):
#     blogs=healthcareblogs.objects.filter(slug=slug)
#     context={
#         "blogs":blogs
#     }
#     return render(request,"blogdetail.html")
# def testcategory(request):
#     tcategories=category.objects.all()
#     context={
#         "categories":tcategories
#     }
#     return render(request,"choose-test-list.html",context)
@login_required(login_url="/login/")   
def prescriptionbookview(request):
    # if request.user.is_anonymous:
    #     # return redirect("user-login")
    #     return HttpResponseRedirect(reverse("user-login"))
    # else:
    c=request.session.get("city")
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse("user-login"))
    fm=prescriptionform()
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
        book=book_history.objects.all().order_by("-created")[0:1]
        # book=book_history.objects.filter(bookingid=bookingid)
        print("=--------",book)
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
        prescription_book(
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
            address=address).save()
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
        data2=Prescriptionbook1.objects.get(unique=unique)
        if myself=="on":
            User.objects.filter(email=request.user.email).update(first_name=firstname,last_name=lastname,phone_no=contact,age=age,address=address)
        data=prescription_book.objects.get(unique=unique)
        print("---",data2.unique)
        book_history(
            user=request.user,
            testbooking_id=data.id,
            uni=data2.bookingid,
            bookingid=bookingid,
            patient_info="myself" if others==None else "others",
                    booking_type="Prescription",
                    bookingdetails="upload prescription",
                    payment_status=False).save()
        
        messages.success(
            request, "Thankyou for your booking!, Our admin team will get back to you shortly.")
        message=f'Hello {request.user.first_name},\n Thank you for Booking!, Our admin team will get back to you shortly. '
            # message = f'Welcome your otp is {otp} '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        subject = "DIGNOSTICA SPAN" 
        send_mail(
                subject,
                message,
                email_from,
                recipient_list,
                fail_silently=False,
        )
        return HttpResponseRedirect(reverse("booking-history"))
        # return render(request,"uploadprescriptions.html",{"fm":fm})
    else:
        return render(request,"uploadprescriptions.html",{"fm":fm})
        
# @login_required(login_url="login/")  
def testselect(request):
    c=request.session.get("city")
    tcategories=category.objects.all()
    tests=test.objects.all()
    envcity={"Bangalore":Bangalore,"Mumbai":Mumbai,"Bhophal":Bhophal,"Nanded":Nanded,"Pune":Pune,"Barshi":Barshi,"Aurangabad":Aurangabad}
    
    context={
        "tests":tests,
        "categories":tcategories,
        "city":c,
        'envcity':envcity
    }
    if request.method=="POST":
        test_name=request.POST.getlist("test_name")
        myself=request.POST.get("myself")
        others=request.POST.get('others')
        others_choice=request.POST.get("others_choice")
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        contact=request.POST.get('contact')
        age=request.POST.get('age')
        gender=request.POST['gender']
        unique = uuid.uuid4()
        s = shortuuid.ShortUUID(alphabet="0123456789")
        bid = s.random(length=5)
        bookingid="DP"+str(bid)
        a=prescription_book.objects.create(
            unique=unique,
            user=request.user,
            
                          myself=True if myself == "on" else False,
                          others=True if others == "on" else False,
                          others_choice=others_choice,
                          firstname=firstname,
                          lastname=lastname,
                          contact=contact,
                          age=age,
                          gender=gender,
                          location=c)
        
        for j in test_name:
            item=test.objects.get(id=j)
            a.test_name.add(item)   
        for i in test_name:
            item=test.objects.get(id=i)
            if c==Bangalore:
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.Banglore_price).save()
            elif c == Mumbai:
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.Mumbai_price).save()
            elif c == Bhophal:
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.bhopal_price).save()   
            elif c == Nanded:
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.nanded_price).save()
            elif c == Pune:
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pune_price).save()
            elif c == Barshi:
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.barshi_price).save()   
            elif c == Aurangabad:
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.aurangabad_price).save()
        messages.success(request,"Your booking added to cart successfully")
        return render(request,"choose-test-list.html",context)
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
    if not request.user.is_anonymous:
        d = cart.objects.filter(device = deviceCookie).update(user=request.user)
    # history=book_history.objects.none()
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
        global uniquee
        uniquee = uuid.uuid4()
        data=cart.objects.filter(user=request.user)
        s = shortuuid.ShortUUID(alphabet="0123456789")
        bid = s.random(length=5)
        # bookingid ="DP"+str(bid)
        book=book_history.objects.all().order_by("-created")[0:1]
        # book=book_history.objects.filter(bookingid=bookingid)
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
        
        b=prescription_book.objects.create(
                unique=uniquee,
                user=request.user,
                myself=True if others == "m" else False,
                others=True if others == "o" else False,
                others_choice=others_choice,
                firstname=firstname,
                lastname=lastname,
                contact=contact,
                age=age,
                gender=gender,
                location=c,
                address=address).save()
        data2=prescription_book.objects.get(unique=uniquee)
        if others=="m":
            User.objects.filter(email=request.user.email).update(first_name=firstname,last_name=lastname,phone_no=contact,age=age,address=address)
        data1=cart.objects.filter(user=request.user)
        # a=[]
        # for i in data:
        #     a.append(i.price)
        request.session.delete("order_id")
        context={}
        amount=request.POST["amount"]
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
        # request.session['amount']=amount
        razorpay_order_id = razorpay_order['id']
        request.build_absolute_uri('/bands/?print=true')
        callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
        # callback_url = 'http://127.0.0.1:8000/paymenthandler/{}/{}/'.format(request.user.email,amount)
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
        listToline = '\n'.join(map(str, strr))
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
                location=c,
                address=address,
                bookingid=bookingid).save()
        data=testbook.objects.get(unique=uniquee) 
        bookhistory=book_history(
                 user=request.user,
                 testbooking_id=data2.id,
                 uni=data.bookingid,
                 bookingid=bookingid,
                 patient_info="Myself" if others == "m" else "others",
                         booking_type="Selected Test/Packages",
                         bookingdetails=listToStr,
                         amount="{0:1.2f}".format(float(amount)),
                         payment_id=razorpay_order_id,
                         payment_status=False).save()
        
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
             couponredeem.objects.create(order_id=razorpay_order_id,coupon=request.session.get("coupon"),discountpercen=request.session.get("couponpercent"),discountamount=request.session.get("discountamount"),actualamount=request.session.get('actualamount')).save()
        if coupon!=None:
            del request.session['coupon']
        if discountamount!=None:
            del request.session['discountamount']
        if couponpercent!=None:
            del request.session['couponpercent']
        if actualamount!=None:
            del request.session['actualamount']
        print(razorpay_order)
        return JsonResponse({"message":True,"razorpay_key":settings.RAZOR_KEY_ID,"currency":currency,"razorpayorder":razorpay_order_id,"callback":callback_url})
    
    if not request.user.is_anonymous:
        c = cart.objects.filter(user=request.user)
    else:
        c = cart.objects.filter(device=deviceCookie)
    data=[]
    for i in c:
        if i.items == None and i.labtest:
            da={}
            da['id']=i.id
            da['test']=i.labtest
            da['price']=str(i.price)
            da["categoryy"]="Health Checks & Lab Tests"
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
            da["categoryy"]="Health Symptoms Pack"
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
        context={
            "data":data,
            "datacount":len(data),
            "subtotal": '{0:1.2f}'.format(sum(a)) 
        }
    except:
         context={
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
        try:
            detail=Prescriptionbook1.objects.get(id=int(testid))
            print("prec")
        except:
            detail=testbook.objects.get(id=int(testid))
            print("test")
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
        # a=paymentids.objects.create(orderid=response_data['razorpay_order_id'],paymentid=response_data['razorpay_payment_id'],signatureid=response_data['razorpay_signature'])
        # a.save()
        return b
    try:
        if request.method =="POST":
            usr=User.objects.get(email=str)
            paymentid=request.POST.get("razorpay_payment_id")
            if paymentid:
                if verify_signature(request.POST):
                    print(paymentid)
                    print(verify_signature)
                    transid=request.POST["razorpay_order_id"]
                    cart.objects.filter(user=usr).delete()
                    history=book_history.objects.get(payment_id=transid)
                    history.payment_status=True
                    Prescriptionbook1.objects.filter(bookingid=history.bookingid).update(payment_status=True)
                    testbook.objects.filter(bookingid=history.bookingid).update(payment_status=True)
                    history.save()
                    payment.objects.create(user=usr,paymentid=paymentid,transid=transid,amount=amount,booking_id=history.bookingid).save()
                    request.session.delete("amount")
                    message1 = f"Hi there,\nWe have successfully received your payment for booking id: {history.bookingid}.\nOur Medical team will get in touch with you for your mentioned tests.\nThank you\nDignostica Span"
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [history.user.email]
                    subject = "DIAGNOSTICA SPAN" 
                    send_mail(
                            f"Payment Successfull| Dignostica Span | Booking Id:{history.bookingid}",
                            message1,
                            email_from,
                            recipient_list,
                            fail_silently=False,
                    )
                    messages.info(request, "Thankyou for making payment our team will come and collect the sample soon.")
                    return HttpResponseRedirect(reverse("booking-history"))
            else:
                b=request.POST.get('error[metadata]')
                c=json.loads(b)
                a=book_history.objects.filter(payment_id=c["order_id"])
                error = request.POST.get('error[description]')
                messages.error(request, error)
                return HttpResponseRedirect(reverse("booking-history"))
    except Exception as e:
        messages.error(request, e)
        return HttpResponseRedirect(reverse("booking-history"))

def subscriptionview(request):
    if request.method=="POST":
        form=subscriptionform()
        if form.is_valid:
            email=request.POST.get("email")
            template_name = 'email.html'
            msg=EmailMessage(
            'Diagnotica',
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
def categoryy(request):
    if request.method=="POST":
        city=request.session.get("city")
        pk=request.POST["pk"]
        searched_name = request.POST.get("searched")
        b=[]

        if pk != "all":
            if searched_name:
                tests=test.objects.filter(categoryy__id=pk, testt__icontains = searched_name)
            else:
                tests=test.objects.filter(categoryy__id=pk)
        else:
            tests=test.objects.all()
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
            print(request.POST)
            city=request.session.get("city")

            searched=request.POST.get('searched')
            req_cat = request.POST.get("cat")
            print(searched)
            if req_cat != "all":
                if searched:
                    tests=test.objects.filter(categoryy__id=req_cat, testt__icontains = searched)
                else:
                    tests=test.objects.filter(categoryy__id=req_cat)
            else:
                tests=test.objects.filter(testt__icontains=searched)

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
            a = cart.objects.get(id=car)  
            a.delete()  
        except:
            pass
                
            # return JsonResponse({"message":True})
        return JsonResponse({"message":"success"})
def coupon(request):
    if request.method=="POST":
        coupon=request.POST.get("coupon")
        total=request.POST.get("total")
        try:
            c=coupons.objects.get(couponcode=coupon,status="a")
            c.discount
            discount=(float(total)*(int(c.discount)/100))
            # print(t)
            totall=float(total)-int(discount)
            request.session['discountamount']=discount
            request.session['coupon']=coupon
            request.session['couponpercent']=c.discount
            request.session['actualamount']=total
            # request.session["couponamount"]=totall
            return JsonResponse({"message":True,"total":float(totall),"percent":c.discount,"discount":"{:.2f}".format(discount)})
        except:
            return JsonResponse({"message":False})
def razorpayclose(request):
    if request.method=="POST":
        paymentid=request.POST["paymentid"]
        a=book_history.objects.filter(payment_id=paymentid)
        b=invoicee.objects.filter(order_id=paymentid)
        c=couponredeem.objects.filter(order_id=paymentid)
        b.delete()
        a.delete()
        c.delete()
        return JsonResponse({"message":True})
    
def contactuss(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        subject=request.POST["subject"]
        message=request.POST["message"]
        contactus.objects.create(fullname=name,email=email,phone=phone,subject=subject,message=message).save()
        message1 = f"Hi {name},\nThank you for contacting us.\nWe have received your query, our internal team will get in touch with you in no time.\nWe welcome you to checkout our top packages in your region till we get back you.\nThank You,\nDignostica Span"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        message = message
        subject = "DIAGNOSTICA SPAN" 
        send_mail(
                "Enquiry | Dignostica Span",
                message1,
                email_from,
                recipient_list,
                fail_silently=False,
        )
        messages.success(request,"Your response submitted successfully")
        return render(request,"contactus.html")
    return render(request,"contactus.html") 
def healthcheckupadd(request):
    cityy=request.session.get("city")
    deviceCookie = request.COOKIES['device']
    RES = {}
    if request.method=="POST":
        if request.POST.get("action") == "healthcheckup":
            slug=request.POST["ids"]
            labtest=healthcheckuppackages.objects.get(id=slug)
            if cityy==Bangalore:
                obj, created = cart.objects.get_or_create(
                    device = deviceCookie,
                    labtest = labtest,
                    user = request.user if not request.user.is_anonymous else None,
                    price=labtest.dBanglore_price
                )
                res = {"message":created}
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
                res = {"message":created}
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
    return render(request,"faq.html",{"faqs":faqss})

def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def invoice(request,orderid):
    order=book_history.objects.get(payment_id=orderid)
    payments=payment.objects.get(transid=orderid)
    try:
        testbooking=Prescriptionbook1.objects.get(bookingid=order.uni)
    except:
        testbooking=testbook.objects.get(bookingid=order.uni)
    invoic=invoicee.objects.filter(order_id=orderid)
    amount=payments.amount
    try:
        coupoonn=couponredeem.objects.get(order_id=orderid)
        couponamount=coupoonn.actualamount
        context_dict={
        
        "order":order,
        "payments":payments,
        "testbooking":testbooking,
        "tests":invoic,
        "coupon":coupoonn,
        "couponamount":num2words(int(float(couponamount)), to = 'ordinal'),
        "amount":num2words(int(float(amount)), to = 'ordinal')
            }
    except:
        # coupoonn=couponredeem.objects.get(order_id=orderid)
        context_dict={
        "order":order,
        "payments":payments,
        "testbooking":testbooking,
        "tests":invoic,
        # "couponamount":num2words(int(couponamount), to = 'ordinal'),
        "amount":num2words(int(float(amount)), to = 'ordinal')
            }
    template_name='invoice2.html'
    pdf = html_to_pdf(template_name,context_dict)
    return FileResponse(pdf,as_attachment=True,filename="invoice2.pdf",content_type='application/pdf') 

from django.contrib.auth.mixins import LoginRequiredMixin
class BookingHistoryPay(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request,*args, **kwargs):
        his = []
        bookhistories=book_history.objects.filter(user=request.user).order_by('-created')
        testbooking=prescription_book.objects.filter(user=request.user)
        payments=payment.objects.filter(user=request.user).order_by('-date')
        for i in bookhistories:
            try:
                testbooking=Prescriptionbook1.objects.get(bookingid=i.uni)
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
                testbooking=testbook.objects.get(bookingid=i.uni)
                # hi['prescription'] = None
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
                # hi['prescription'] = testbooking.prescription_file
                hi['payment_status'] = i.payment_status
                try:
                    hi['report'] = testbooking.report
                except:
                    hi['report'] = None
                hi['amount'] = i.amount
                his.append(hi)

        context={
            "bookhistories":his,
            "bookinghistorylength":len(his),
            "paymentcount":payments.count(),
            "payments":payments,
            "testbooking":testbooking,
        }
        return render(request,"booking-history.html",context)
    def post(self, request, *args, **kwargs):
        if request.POST.get("action") == "retreive_data":
            id=request.POST.get('id')
            mod = book_history.objects.get(uni=id)
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            tot_amt = float(mod.amount) * 100
            razorpay_order = client.order.create(
                {"amount": tot_amt, "currency": "INR", "payment_capture": "1"}
            )
            mod.payment_id = razorpay_order['id']
            mod.save()
            callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,tot_amt//100))
            to_return = {
                "razorKey":settings.RAZOR_KEY_ID,
                "valid":True,
                "amount":tot_amt,
                "order_id":razorpay_order['id'],
                "callbackUrl":callback_url,
            }
            try:
                items=Prescriptionbook1.objects.get(bookingid=id)
            except:
                items=testbook.objects.get(bookingid=id)
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
        
        if request.POST.get("action") == "payment_canceled":
            mod = book_history.objects.get(testbooking_id=request.POST.get('id'))
            mod.payment_id = None
            mod.payment_status = False
            mod.save()
            to_return = {"valid":True}
        return HttpResponse(json.dumps(to_return), content_type="application/json")


class HealthSymptoms(View):
    def get(self, request, *args,**kwargs):
        c=request.session.get("city")
        currentSymptom = kwargs['slug']
        currentObj = healthsymptoms.objects.get(slug = currentSymptom)
        obj = healthsymptoms.objects.exclude(slug = currentSymptom)
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
            price=healthSympObj.Banglore_price,)
            res = {"message":created}
            RES = res

        elif cityy == Mumbai:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.Mumbai_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Bhophal:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.bhopal_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Nanded:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.nanded_price,
            )
            res = {"message":created}
            RES = res
            
        elif cityy == Pune:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.pune_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Barshi:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.barshi_price,
            )
            res = {"message":created}
            RES = res
        elif cityy == Aurangabad:
            obj, created = cart.objects.get_or_create(
            device = deviceCookie,
            packages = healthSympObj,
            user = request.user if not request.user.is_anonymous else None,
            price=healthSympObj.aurangabad_price,
            )
            res = {"message":created}
            RES = res
        if request.user.is_anonymous:
            request.session['cart_count']= cart.objects.filter(device = deviceCookie).count()
        else:
            request.session['cart_count']= cart.objects.filter(user = request.user).count()
        print(RES)
        return JsonResponse(RES)
def privacypolicy(request):
    return render(request,"privacypolicy.html")
def paymentsrefund(request):
    return render(request,"paymentsrefunds.html")
def termsofuse(request):
    return render(request,"termsofuse.html")
def error_404_view(request, exception):
    return HttpResponse("404 Not Found")


