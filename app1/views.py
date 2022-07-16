import re
from django.shortcuts import render,redirect
from .forms import UserProfileForm,UserRegistrationForm, forgotpasswordform, prescriptionform, selectedtestform, subscriptionform
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

global OBJ_COUNT
OBJ_COUNT = 0
checkk=[]
teest=[]
packagee=[]
def dashboard(request):
    test=prescription_book.objects.all().count()
    test_bookings=prescription_book.objects.exclude(test_name__isnull=True,prescription_file__isnull=False).count()
    prescription_bookings=prescription_book.objects.exclude(test_name__isnull=False,prescription_file__isnull=True).count()
    packages=healthpackages.objects.all().count()
    context={
        "test":test,
        "test_bookings":test_bookings,
        "prescription_bookings":prescription_bookings,
        "packages":packages,
    }
    return HttpResponse(json.dumps(context),content_type="application/json")
def aboutus(request):
    return render (request,"aboutus.html")
def cityy(request):
    city=request.POST["city"]
    print(city)
    request.session["city"]=city
    return JsonResponse({"message":True,"city":city})
    # if request.method =="GET":
    #     cit=city.objects.all()
    #     healthcheckup=healthcheckuppackages.objects.all()
    #     healthpackage=healthpackages.objects.all()
    #     healthsymptom=healthsymptoms.objects.all()
    #     healthcareblog=healthcareblogs.objects.all()
    #     testimonial=testimonials.objects.all()
    #     context={
    #         "healthcheckup":healthcheckup,
    #         "healthpackage":healthpackage,
    #         "healthsymptom":healthsymptom,
    #         "testimonial":testimonial,
    #         "healthcareblog":healthcareblog,
    #         "city":cit,
    #     }
    #     return render(request,'home.html',context)
    
def Registration(request):
    if request.method == "POST":
        print("dataa")
        fm = UserRegistrationForm(request.POST)
        up = UserProfileForm(request.POST)
        # if fm.is_valid():
        e = request.POST['email']
        u = request.POST['name']
        p = request.POST['confirmpassword']
        user=User.objects.filter(email=e)
        if user.exists():
            messages.error(request,"Email is already registered")
            return render(request,'register.html')
        else:
            request.session['email'] = e
            request.session['username'] = u
            request.session['password'] = p
            p_number = request.POST['phone']
            request.session['number'] = p_number
            otp = random.randint(1000,9999)
            request.session['otp'] = otp
                # message = f'your otp is {otp}'
                # send_otp(p_number,message)
            message = f'Welcome your otp is {otp} '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            message = message
            subject = "OTP" 
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
    if request.method == "POST":
        u_otp1 = request.POST['digit-1']
        u_otp2 = request.POST['digit-2']
        u_otp3 = request.POST['digit-3']
        u_otp4 = request.POST['digit-4']
        a=str(u_otp1)+str(u_otp2)+str(u_otp3)+str(u_otp4)
        print(a)
        otp = request.session.get('otp')
        user = request.session['username']
        # hash_pwd=request.session.get('password')
        hash_pwd = make_password(request.session.get('password'))
        p_number = request.session.get('number')
        email_address = request.session.get('email') 

        if int(a) == otp:
            User.objects.create(
                            username = user,
                            email=email_address,
                            phone_no=p_number,
                            password=hash_pwd
            )
            request.session.delete('otp')
            request.session.delete('user')
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
    message = f'Welcome your resend otp is {otp} '
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
    return redirect('/registration/otp/')

def changepassword(request):
    if request.method=="POST":
      password=request.POST["currentPassword"]
      conpassword=request.POST["confirmpassword"]
       
      otp = random.randint(1000,9999)
      print(otp)
      email_address = request.user.email
      a=authenticate(request,username=request.user.email,password=password)
      if a == None:
          messages.info(request,"Invalid password")
          return render (request,"changepassword.html")
      else:
        request.session["ppassword"]=password 
        request.session["conpassword"]=conpassword
        request.session['otp'] = otp
        message = f'Welcome your resend otp is {otp} '
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
            message = f'Welcome your forgot password otp is {otp} '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [e]
            message = message
            subject = "OTP" 
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
    if request.method == "POST":
        u_otp1 = request.POST['digit-1']
        u_otp2 = request.POST['digit-2']
        u_otp3 = request.POST['digit-3']
        u_otp4 = request.POST['digit-4']
        a=str(u_otp1)+str(u_otp2)+str(u_otp3)+str(u_otp4)
        print(a)
        otp = request.session.get('otp')
        
        # user = request.session['username']
        # hash_pwd=request.session.get('password')
        hash_pwd = make_password(request.session.get('password'))
        # p_number = request.session.get('number')
        email_address = request.session.get('email') 
        password=request.session.get("ppassword")
        # request.session.get("newpassword")
        newpassword=make_password(request.session.get("conpassword"))
        if int(a) == otp:
            data = User.objects.filter(
                            email=request.user.email,password=password)
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
            print("changed successfully")
            # messages.success(request,'Password changed successfully!!')
            return redirect('home')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'otpforgot.html')    
def passwordcheck(request):
    if request.method=="POST":
        password=request.POST.get("password")
        # print(password)
        try:
            a=authenticate(request,username=request.user.email,password=password)
            if a == None:
            # User.objects.get(email=request.user.email,password=password) 
                return JsonResponse({"message":False})
                
            else:
                return JsonResponse({"message":True})
        except Exception as e: 
            print(e)
            return JsonResponse({"message":False})

              
def otpforgotpassword(request):
    if request.method == "POST":
        u_otp1 = request.POST['digit-1']
        u_otp2 = request.POST['digit-2']
        u_otp3 = request.POST['digit-3']
        u_otp4 = request.POST['digit-4']
        a=str(u_otp1)+str(u_otp2)+str(u_otp3)+str(u_otp4)
        print(a)
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
            return redirect('user-login')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'otpforgot.html') 
    
def forgotresendotp(request):
    # if request.method=="POST":
    email_address = request.session.get('email')
    otp = random.randint(1000,9999)
    request.session['otp'] = otp
    message = f'Welcome your resend otp is {otp} '
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
   print(a)
   
   return JsonResponse({"message":True,"firstname":a.first_name,"lastname":a.last_name,"contact":a.phone_no,"gender":a.gender,"address":a.address,"age":a.age}) 
def profilee(request):
    profile=User.objects.get(email=request.user.email)
    print(profile.email)
    print(profile.address)
    context={
        "profile":profile,
    }
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        gender=request.POST.get("gender")
        location=request.POST.get("location")
        age=request.POST.get("age")
        address=request.POST.get("address")
        User.objects.filter(email=request.user.email).update(username=name,
                                                             email=email,
                                                             phone_no=phone,
                                                             gender=gender,
                                                             location=location,
                                                             age=age,
                                                             address=address)
        
        messages.success(request,"Profile updated Successfully")
        profile=User.objects.get(email=request.user.email)
        context1={
            "profile":profile,
        }
        return render (request,"profile.html",context1)  
        
    return render (request,"profile.html",context)          
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
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request,username=username,password=password)
        a=request.session.get("cartt")
        print(a)
        
        if user is not None:
            login(request,user)
            a=request.session.get("cartt")
            city=request.session.get("city")
            try:
                chckupp=healthcheckuppackages.objects.filter(id__in=a.get("checkup"))
            except:
                package=healthpackages.objects.filter(id__in=a.get("package"))
                tessst=test.objects.filter(id__in=a.get("selecttest"))
            try:
                package=healthpackages.objects.filter(id__in=a.get("package"))
            except:
                chckupp=healthcheckuppackages.objects.filter(id__in=a.get("checkup"))
                tessst=test.objects.filter(id__in=a.get("selecttest"))
            try:
                tessst=test.objects.filter(id__in=a.get("selecttest"))
            except:
                package=healthpackages.objects.filter(id__in=a.get("package"))
                chckupp=healthcheckuppackages.objects.filter(id__in=a.get("checkup"))
            # context["chckupp"]=chckupp
            # context["package"]=package
            # context["tessst"]=tessst
            
            # cart.objects.create(user=request.user,items=tes,categoryy=tes.categoryy,price=tes.pricel1).save()
            # print(chckupp)
            # print(package)
            # print(tessst)
            for j in chckupp:
                
                if city=="Bangalore":
                    price=str(j.dpricel1)
                   
                elif city == "Chennai":
                    price=str(j.dpricel1)
                   
                elif city == "Mumbai":
                    price=str(j.dpricel1)
                   
                elif city == "Delhi":
                    price=str(j.dpricel1)
                    
                cart.objects.create(user=request.user,labtest=j,price=price).save()
               
                
            for j in package:
                
                if city=="Bangalore":
                   
                    price=str(j.pricel1)
                elif city == "Chennai":
                    
                    price=str(j.pricel1)
                elif city == "Mumbai":
                    
                    price=str(j.pricel1)
                elif city == "Delhi":
                    
                    price=str(j.pricel1)
                cart.objects.create(user=request.user,packages=j,price=price).save()
               
                
            for j in tessst:
                print("--------",j)
                if city=="Bangalore":
                    price=str(j.pricel1)
                    
                elif city == "Chennai":
                    price=str(j.pricel1)
                  
                elif city == "Mumbai":
                    price=str(j.pricel1)
                   
                elif city == "Delhi":
                    price=str(j.pricel1)
                    print("--------",j)
                cart.objects.create(user=request.user,items=j,price=price,categoryy=j.categoryy).save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)  
            # return redirect('/')
        else:
            messages.error(request,'Email or password is wrong')
    return render(request,'login.html')

def booktestonline(request):
    return render(request,"book-test-online.html")
from django.contrib.auth import logout
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
    request.session['cartt']={
        "checkup":[],
        "package":[],
        "selecttest":[]
       }
    print(request.session.get("city"))
    c=request.session.get("city")
    print(".....",request.user)
    if request.method =="GET":
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
        }
        
        return render(request,'home.html',context)
    # if request.POST.get("action") == "retreive_data":
    #     currentcity=request.session.get("city")
    #     slug=request.POST['id']
    #     print(slug)
    #     context={}
    #     healthcheckup=healthcheckuppackages.objects.get(slug=slug)
    #     if currentcity=="Bangalore":
    #         amount=healthcheckup.dpricel1
    #     elif currentcity=="Chennai":
    #         amount=healthcheckup.dpricel2
    #     elif currentcity=="Mumbai":
    #         amount=healthcheckup.dpricel3
    #     elif currentcity=="Delhi":
    #         amount=healthcheckup.dpricel4
        
        
    #     return JsonResponse(context)
    # else:
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
        }
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
    city=request.session.get("city")
    context={
        "packages":packages,
        "city":city,
    }
    return render(request,'healthpackages.html',context)

def healthpackageview(request,slug):
        c=request.session.get("city")
        package=healthpackages.objects.get(slug=slug)
        packages=healthpackages.objects.exclude(slug=slug)
        context={
            "package":package,
            "packages":packages,
            "city":c
        }
        currency = 'INR'
        if c == "Bangalore":
            amount=int(package.pricel1)
        elif c == "Chennai":
            amount=int(package.pricel2)
        elif c == "Mumbai":
            amount=int(package.pricel3)
        elif c == "Delhi":
            amount=int(package.pricel4)
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
        # context['callback_url'] = callback_url
        # bookhistory=book_history(
        #     user=request.user,
        #              booking_type="Package",
        #              bookingdetails=slug,
        #              patient_info="Myself",
        #              amount=amount,
        #              payment_id=razorpay_order['id'],
        #              payment_status=False).save()
        print("booked")
        return render(request,'packagedetail.html',context)

# def healthpackageview(request,slug):
#     if request.user.is_anonymous:
#         return HttpResponseRedirect(reverse("user-login"))
#     else:
#         c=request.session.get("city")
#         package=healthpackages.objects.get(slug=slug)
#         packages=healthpackages.objects.exclude(slug=slug)
#         context={
#             "package":package,
#             "packages":packages,
#             "city":c
#         }
#         currency = 'INR'
#         if c == "Bangalore":
#             amount=int(package.pricel1)
#         elif c == "Chennai":
#             amount=int(package.pricel2)
#         elif c == "Mumbai":
#             amount=int(package.pricel3)
#         elif c == "Delhi":
#             amount=int(package.pricel4)
#         client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#         try:
#             razorpay_order = client.order.create(
#                     {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#             )
#         except Exception as e:
#             razorpay_order = client.order.create(
#                     {"amount": 1* 100, "currency": "INR", "payment_capture": "1"}
#             )
#         request.session['amount']=amount
#         razorpay_order_id = razorpay_order['id']
#         callback_url = callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
#         context['razorpay_order_id'] = razorpay_order_id
#         context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#         context['razorpay_amount'] = amount
#         context['currency'] = currency
#         context['callback_url'] = callback_url
#         bookhistory=book_history(
#             user=request.user,
#                      booking_type="Package",
#                      bookingdetails=slug,
#                      patient_info="Myself",
#                      amount=amount,
#                      payment_id=razorpay_order['id'],
#                      payment_status=False).save()
#         print("booked")
#         return render(request,'packagedetail.html',context)
def testdetails(request):
    if request.method=="POST":
            id=request.POST["id"]
            a=book_history.objects.get(id=id)
            return JsonResponse({"message":a.bookingdetails})
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
    detail=healthcareblogs.objects.first()
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
    # print(request.FILES)
    fm=prescriptionform()
    if request.method=="POST":
        print(request.POST)
        prescription_file=request.FILES.get("file")
        print()
        myself=request.POST.get("radio_self")
        others=request.POST.get('radio_others')
        others_choice=request.POST.get("option")
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        contact=request.POST.get('phone')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        unique = uuid.uuid4()
        print(unique)
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
                        location=c).save()
        data=prescription_book.objects.get(unique=unique)
        print(data)
        book_history(
            user=request.user,
            testbooking_id=data.id,
            patient_info="myself" if others==None else "others",
                    booking_type="Prescription",
                    bookingdetails="upload prescription",
                    payment_status=False).save()
        messages.success(request,"Your response is recorded successfully")
        return HttpResponseRedirect(reverse("booking-history"))
        # return render(request,"uploadprescriptions.html",{"fm":fm})
    else:
        return render(request,"uploadprescriptions.html",{"fm":fm})
        
# @login_required(login_url="login/")  
def testselect(request):
    c=request.session.get("city")
    print("-----",city)
    tcategories=category.objects.all()
    tests=test.objects.all()
    print(request.method)
    context={
        "tests":tests,
        "categories":tcategories,
        "city":c,
    }
    if request.method=="POST":
        # others=request.POST.get("myself")
        print(request.POST)
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
            if c=="Banglore":
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel1).save()
            elif c == "Chennai":
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel2).save()
            elif c == "Mumbai":
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel3).save()   
            elif c == "Delhi":
                cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel4).save() 
        messages.success(request,"Your booking added to cart successfully")
        return render(request,"choose-test-list.html",context)
    return render(request,"choose-test-list.html",context)
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# @login_required(login_url="login/")    
def cartt(request):
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
        print(address)
        global uniquee
        uniquee = uuid.uuid4()
        data=cart.objects.filter(user=request.user)
        a=prescription_book.objects.create(
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
                                location=c)
        data2=prescription_book.objects.get(unique=uniquee)
        if others=="m":
            User.objects.filter(email=request.user.email).update(first_name=firstname,last_name=lastname,phone_no=contact,age=age,address=address)
        data1=cart.objects.filter(user=request.user)
        a=[]
        for i in data:
            a.append(i.price)
        def testname():
            return ", ".join([
                test.testt for test in data2.test_name.all()
            ])
            
        def testname():
            return ",".join([
                test.testt for test in data1
            ])
        strr=[]
        for tesst in data1:
            if tesst.items == None and tesst.packages == None:
                strr.append(tesst.labtest.package_title)
            elif tesst.items == None and tesst.labtest == None:
                strr.append(tesst.packages.package_name)
            else:
                strr.append(tesst.items.testt)
        listToStr = ','.join(map(str, strr))
        # str1 = " " 
        # for i in str:
        #     str1 += i
        request.session.delete("order_id")
        data=cart.objects.filter(user=request.user)
        a=[]
        for i in data:
            a.append(i.price)
        context={}
        amount=request.POST["amount"]
       
        currency = 'INR'
        # amount=int(sum(a))
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
        print("-----",razorpay_order_id)
        request.build_absolute_uri('/bands/?print=true')
        callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
        # callback_url = 'http://127.0.0.1:8000/paymenthandler/{}/{}/'.format(request.user.email,amount)
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        bookhistory=book_history(
            user=request.user,
            testbooking_id=data2.id,
            patient_info="Myself" if others == "m" else "others",
                     booking_type="Selected test",
                     bookingdetails=listToStr,
                     amount=sum(a),
                     payment_id=razorpay_order_id,
                     payment_status=False).save()
        return JsonResponse({"message":True,"razorpay_key":settings.RAZOR_KEY_ID,"currency":currency,"razorpayorder":razorpay_order_id,"callback":callback_url})
    # data1=cart.objects.filter(user=request.user)
    # a=[]
    # for i in data1:
    #     a.append(i.price)
    # context={
    #         "data":data1,
    #        "subtotal":sum(a),
    #         "datacount":data1.count(),
    #         }
    # print(request.session.get("cartt"))
    a=request.session.get("cartt")
    print(request.user.is_anonymous)
    if request.user.is_anonymous==True:
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
       
        data= []
        city=request.session.get("city")
        try:
            for j in chckupp:
                da={}
                da['cat']="checkup"
                da["id"]=j.id
                da["test"]=j.package_title
                if city == "Bangalore":
                    da["price"]=str(j.dpricel1)
                elif city == "Chennai":
                    da["price"]=str(j.dpricel2)
                elif city == "Mumbai":
                    da["price"]=str(j.dpricel3)
                elif city == "Delhi":
                    da["price"]=str(j.dpricel4)
                data.append(da)
        except:
            pass
        try:
            for j in package:
                da={}
                da['cat']="package"
                da["id"]=j.id
                da["test"]=j.package_name
                if city == "Bangalore":
                    da["price"]=str(j.pricel1)
                elif city == "Chennai":
                    da["price"]=str(j.pricel2)
                elif city == "Mumbai":
                    da["price"]=str(j.pricel3)
                elif city == "Delhi":
                    da["price"]=str(j.pricel4)
                data.append(da)
        except:
            pass
        try:
            for j in tessst:
                da={}
                da['cat']="selecttest"
                da["id"]=j.id
                da["test"]=j.testt
                if city == "Bangalore":
                    da["price"]=str(j.pricel1)
                elif city == "Chennai":
                    da["price"]=str(j.pricel2)
                elif city == "Mumbai":
                    da["price"]=str(j.pricel3)
                elif city == "Delhi":
                    da["price"]=str(j.pricel4)
                da["categoryy"]=j.categoryy
                data.append(da)
            print(data)
        except:
            pass
        a=[]
        try:
            for i in data:
                print(i["price"])
                a.append(float(i["price"]))
            context={
            "data":data,
            "subtotal":sum(a)
        }
        except:
            context={
                
            }
        return render(request,"mycart.html",context) 
    
    elif request.user.is_anonymous == False:
        # try:
        data=[]
        for i in cart.objects.filter(user=request.user):
            if i.items == None and i.labtest == None:
                da={}
                da['id']=i.id
                da['test']=i.packages
                da['price']=str(i.price)
                data.append(da)
            elif i.items == None and i.packages == None:
                da={}
                da['id']=i.id
                da['test']=i.labtest
                da['price']=str(i.price)
                data.append(da)
            elif i.labtest == None and i.packages == None: 
                da={}
                da['id']=i.id
                da['test']=i.items
                da['price']=str(i.price)  
                da["categoryy"]=i.categoryy
                data.append(da)
        
        a=[]
        for i in data:
            print(i["price"])
            a.append(float(i["price"]))
        context={
            "data":data,
            "subtotal":sum(a)
        }
        print("------",data)
        return render(request,"mycart.html",context)
        # except:
        #     return render(request,"mycart.html")
    

def cartsessiondelete(request):
    if request.method=="POST":
        if request.POST.get("action")=="forsession":
        # if request.user.is_anonymous==True:
            id=request.POST["pk"]
            s=id.split("-")
            a=request.session.get("cartt")
            b=a.get(s[1])
            print(b)
            if s[0] in b:
                
                b=a.get(s[1])
                print("-----------------------",s[1])
                b.remove(s[0])
                print(b)
                print("-------------------------")
                return JsonResponse({"message":True})
        elif request.POST.get("action")=="fordatabse":
        # elif request.user.is_anonymous == False:
            pk=request.POST["pk"]
            print(pk)
            a = cart.objects.get(id=pk)  
            print(a)
            a.delete()  
            print("deleted")
            # return redirect("cart")
            return JsonResponse({"message":"success"})
        # elif request.POST.get("action")=="fordatabse":
        #     if request.user.is_anonymous==True:
        #         id=request.POST["pk"]
        #         s=id.split("-")
        #         a=request.session.get("cartt")
        #         b=a.get(s[1])
        #         print(b)
        #         if s[0] in b:
                    
        #             b=a.get(s[1])
        #             print("-----------------------",s[1])
        #             b.remove(s[0])
        #             print(b)
        #             print("-------------------------")
        #             return JsonResponse({"message":True})
        #     elif request.user.is_anonymous == False:
        #         pk=request.POST["pk"]
        #         print(pk)
        #         a = cart.objects.get(id=pk)  
        #         print(a)
        #         a.delete()  
        #         print("deleted")
        #         # return redirect("cart")
        #         return JsonResponse({"message":"success"})
@login_required(login_url="login/")    
def cartt1(request):
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
        print(address)
        global uniquee
        uniquee = uuid.uuid4()
        data=cart.objects.filter(user=request.user)
        a=prescription_book.objects.create(
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
                                location=c)
        data2=prescription_book.objects.get(unique=uniquee)
        if others=="m":
            User.objects.filter(email=request.user.email).update(first_name=firstname,last_name=lastname,phone_no=contact,age=age,address=address)
        data1=cart.objects.filter(user=request.user)
        a=[]
        for i in data:
            a.append(i.price)
        def testname():
            return ", ".join([
                test.testt for test in data2.test_name.all()
            ])
            
        def testname():
            return ",".join([
                test.testt for test in data1
            ])
        strr=[]
        for tesst in data1:
            if tesst.items == None and test.packages == None:
                strr.append(tesst.labtest.package_title)
            elif tesst.items == None and test.labtest == None:
                strr.append(tesst.packages.package_name)
            else:
                strr.append(tesst.items.testt)
        listToStr = ','.join(map(str, strr))
        # str1 = " " 
        # for i in str:
        #     str1 += i
        request.session.delete("order_id")
        data=cart.objects.filter(user=request.user)
        a=[]
        for i in data:
            a.append(i.price)
        context={}
        amount=request.POST["amount"]
       
        currency = 'INR'
        # amount=int(sum(a))
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
        print("-----",razorpay_order_id)
        request.build_absolute_uri('/bands/?print=true')
        callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
        # callback_url = 'http://127.0.0.1:8000/paymenthandler/{}/{}/'.format(request.user.email,amount)
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        bookhistory=book_history(
            user=request.user,
            testbooking_id=data2.id,
            patient_info="Myself" if others == "m" else "others",
                     booking_type="Selected test",
                     bookingdetails=listToStr,
                     amount=sum(a),
                     payment_id=razorpay_order_id,
                     payment_status=False).save()
        return JsonResponse({"message":True,"razorpay_key":settings.RAZOR_KEY_ID,"currency":currency,"razorpayorder":razorpay_order_id,"callback":callback_url})
    # data=cart.objects.filter(user=request.user)
    # a=[]
    # for i in data:
    #     a.append(i.price)
    # context={
    #         "data":data,
    #        "subtotal":sum(a),
    #         "datacount":data.count(),
    #         }
    # print(request.session.get("cartt"))
    a=request.session.get("cartt")
    # print(a.get("checkup"))
    context={}
    chckupp=healthcheckuppackages.objects.filter(id__in=a.get("checkup"))
    package=healthpackages.objects.filter(id__in=a.get("package"))
    tessst=test.objects.filter(id__in=a.get("selecttest"))
    context["chckupp"]=chckupp
    context["package"]=package
    context["tessst"]=tessst
    for i in [chckupp,package,package]:
        for j in i:
            print(j)
    return render(request,"mycart.html",context)
def othersdetail(request):
    if request.method=="POST":
        testid=request.POST["testid"]
        print(testid)
        detail=prescription_book.objects.get(id=int(testid))
        print(detail.firstname)
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
        return JsonResponse({"message":True,"firstname":detail.firstname,"lastname":detail.lastname,"gender":detail.gender,"otherschoice":choice,"age":detail.age,"phone":detail.contact})
@csrf_exempt
def paymenthandler(request,str,amount):
    # if request.method =="POST":
    #     print(str)
    #     usr=User.objects.get(email=str)
    #     paymentid=request.POST["razorpay_payment_id"]
    #     transid=request.POST["razorpay_order_id"]
    #     print(amount)
    #     cart.objects.filter(user=usr).delete()
    #     payment.objects.create(user=usr,paymentid=paymentid,transid=transid,amount=amount).save()
    #     history=book_history.objects.get(payment_id=transid)
    #     history.payment_status=True
    #     history.save()
    #     request.session.delete("amount")
    #     request.session.delete("couponamount")
    #     messages.info(request, "Thank You, your Payment was successful")

    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        b = client.utility.verify_payment_signature(response_data)
        return b
    try:
        if request.method =="POST":
            usr=User.objects.get(email=str)
            paymentid=request.POST.get("razorpay_payment_id")
            if paymentid:
                print(request.POST)
                if verify_signature(request.POST):
                    transid=request.POST["razorpay_order_id"]
                    cart.objects.filter(user=usr).delete()
                    payment.objects.create(user=usr,paymentid=paymentid,transid=transid,amount=amount).save()
                    history=book_history.objects.get(payment_id=transid)
                    history.payment_status=True
                    history.save()
                    request.session.delete("amount")
                    messages.info(request, "Thank You, your Payment was successful")
                    return HttpResponseRedirect(reverse("booking-history"))
            else:
                b=request.POST.get('error[metadata]')
                c=json.loads(b)
                print(c["order_id"])
                a=book_history.objects.filter(payment_id=c["order_id"])
                print("deleted")
                error = request.POST.get('error[description]')
                messages.error(request, error)
                return HttpResponseRedirect(reverse("booking-history"))
    except Exception as e:
        print(e)
        messages.error(request, e)
        return HttpResponseRedirect(reverse("booking-history"))

def subscriptionview(request):
    if request.method=="POST":
        form=subscriptionform()
        if form.is_valid:
            email=request.POST.get("email")
            template_name = 'email.html'
            msg=EmailMessage(
            'Prakash Electricals',
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
from functools import wraps


def addtocart(request):
        if request.method=="POST":
            cityy=request.session.get("city")
            if request.user.is_anonymous == True:
                pk=request.POST["pk"]
                item=test.objects.get(id=pk)
                
                if str(item.id) in request.session['cartt']['selecttest']:
                    return JsonResponse({"message":False})
                else:
                    print("iiiiii")
                    teest.append(str(item.id))
                    request.session['cartt']['selecttest']=teest
                print( request.session['cartt'],"AAGIN")
                request.session.modified = True
                return JsonResponse({"message":True})
            elif request.user.is_anonymous==False:
                pk=request.POST["pk"]
                item=test.objects.get(id=pk)
                data=cart.objects.filter(items=item)
                if data.exists():
                   return JsonResponse({"message":False}) 
                if cityy=="Bangalore":
                    cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel1).save()
                elif cityy=="Chennai":
                    cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel2).save()
                elif cityy=="Mumbai":
                    cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel3).save()
                elif cityy=="Delhi":
                    cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel4).save()
                return JsonResponse({"message":True})


def categoryy(request):
    print(request.method)
    if request.method=="POST":
        city=request.session.get("city")
        pk=request.POST["pk"]
        b=[]
        
        
        tests=test.objects.filter(categoryy__id=pk)
        # print(tests)
        for tesst in tests:
            a={}
            
            a['id']=tesst.id
            a['testt']=tesst.testt
            a['description']=tesst.description
            if city == "Bangalore":
                a["pricel1"]=str(tesst.pricel1)
            elif city== "Chennai":
                a["pricel1"]=str(tesst.pricel2)
            elif city== "Mumbai":
                a["pricel1"]=str(tesst.pricel3)
            elif city== "Delhi":
                a["pricel1"]=str(tesst.pricel3)
            print(a)
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
            searched=request.GET.get('searched')
            searched=request.POST["searched"]
            tcategories=category.objects.all()
            b=[]
            tests=test.objects.filter(testt__icontains=searched)
            for tesst in tests:
                a={}
                
                a["id"]=tesst.id
                a["testt"]=tesst.testt
                a["description"]=tesst.description
                if city == "Bangalore":
                    a["pricel1"]=str(tesst.pricel1)
                if city== "Chennai":
                    a["pricel1"]=str(tesst.pricel2)
                if city== "Mumbai":
                    a["pricel1"]=str(tesst.pricel3)
                if city== "Delhi":
                    a["pricel1"]=str(tesst.pricel3)
                b.append(a)
            print(b)
            return JsonResponse(b,safe=False)
    else:
        return render(request,"choose-test-list.html") 
       
def destroy(request): 
    if request.method=="POST":
        pk=request.POST["pk"]
        print(pk)
        a = cart.objects.get(id=pk)  
        print(a)
        a.delete()  
        print("deleted")
        # return redirect("cart")
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
            request.session["couponamount"]=totall
            return JsonResponse({"message":True,"total":totall,"percent":c.discount,"discount":"{:.2f}".format(discount)})
        except:
            return JsonResponse({"message":False})
def razorpayclose(request):
    if request.method=="POST":
        paymentid=request.POST["paymentid"]
        print(paymentid)
        a=book_history.objects.filter(payment_id=paymentid)
        print(a)
        a.delete()
        print("deleted")
        return JsonResponse({"message":True})
def contactuss(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        subject=request.POST["subject"]
        message=request.POST["message"]
        contactus.objects.create(fullname=name,email=email,phone=phone,subject=subject,message=message).save()
        # messages.success(request,"Your response submitted successfully")
        return render(request,"contactus.html")
    return render(request,"contactus.html") 
def healthcheckupadd(request):
    cityy=request.session.get("city")
    if request.method=="POST":
        if request.user.is_anonymous==True:
            if request.POST.get("action") == "healthcheckup":
                slug=request.POST["slug"]
                labtest=healthcheckuppackages.objects.get(slug=slug)
            
                if str(labtest.id) in request.session['cartt']['checkup']:
                    return JsonResponse({"message":False})
                # request.session['cartt']['checkup'] += [str(labtest.id)]
                else:
                    checkk.append(str(labtest.id))
                    request.session['cartt']['checkup']=checkk
                print( request.session['cartt'],"AAGIN")
                request.session.modified = True
                return JsonResponse({"message":True})
            elif request.POST.get("action") == "healthpackage":
                slug=request.POST["slug"]
                package=healthpackages.objects.get(slug=slug)
                request.session['cartt'].update({"package":[]})
                if str(package.id) in request.session['cartt']['package']:
                    return JsonResponse({"message":False})
                else:
                    packagee.append(str(package.id))
                    request.session['cartt']['package']=packagee
                print( request.session['cartt'],"AAGIN")
                request.session.modified = True
                return JsonResponse({"message":True})
        if request.user.is_anonymous==False:
            city=request.session.get('city')
            if request.POST.get("action") == "healthcheckup":
                slug=request.POST["slug"]
                labtest=healthcheckuppackages.objects.get(slug=slug)
                data=cart.objects.filter(labtest=labtest)
                if data.exists():
                    return JsonResponse({"message":False})
                else:
                    if city=="Bangalore":
                        cart.objects.create(user=request.user,labtest=labtest,price=labtest.dpricel1).save()
                    elif city == "Chennai":
                        cart.objects.create(user=request.user,labtest=labtest,price=labtest.dpricel2).save()
                    elif city == "Mumbai":
                        cart.objects.create(user=request.user,labtest=labtest,price=labtest.dpricel3).save()
                    elif city == "Delhi":
                        cart.objects.create(user=request.user,labtest=labtest,price=labtest.dpricel4).save()
                    return JsonResponse({"message":True})
            elif request.POST.get("action") == "healthpackage":
                slug=request.POST["slug"]
                package=healthpackages.objects.get(slug=slug)
                data=cart.objects.filter(packages=package)
                if data.exists():
                    return JsonResponse({"message":False})
                else:
                    if city=="Bangalore":
                        cart.objects.create(user=request.user,packages=package,price=package.pricel1).save()
                    elif city == "Chennai":
                        cart.objects.create(user=request.user,packages=package,price=package.pricel2).save()
                    elif city == "Mumbai":
                        cart.objects.create(user=request.user,packages=package,price=package.pricel3).save()
                    elif city == "Delhi":
                        cart.objects.create(user=request.user,packages=package,price=package.pricel4).save()
                    return JsonResponse({"message":True})
        #cart.objects.create(labtest=data,price=data.)
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
    print(order)
    payments=payment.objects.get(transid=orderid)
    
    # print(data)
    context_dict={
        "order":order,
        "payments":payments
            # "order_id":order.order_payment_id,
            # "payment_id":paymentid.payment_id,
            # "date":order.date,
            # "total_price":amount,
            # "data":data,
            # "gst":gst,
            # "grand_total":grand_total,
            # "deliver_charge":deliver_charge,
            # "name":address.fullname,
            # "phone":address.phone,
            # "locality":address.locality,
            # "address":address.address,
            # "city":address.city,
            # "state":address.state,
            # "pincode":address.pincode
            }
    template_name='invoice.html'
    pdf = html_to_pdf(template_name,context_dict)
    print(pdf)
    return FileResponse(pdf,as_attachment=True,filename="invoice.pdf",content_type='application/pdf') 

# def otpLogin(request):
#     if request.method == "POST":
#         username = request.session['username']
#         password = request.session['password']
#         otp = request.session.get('login_otp')
#         u_otp = request.POST['otp']
#         if int(u_otp) == otp:
#             user = authenticate(request,username=username,password=password)
#             if user is not None:
#                 login(request,user)
#                 request.session.delete('login_otp')
#                 messages.success(request,'login successfully')
#                 return redirect('/')
#         else:
#             messages.error(request,'Wrong OTP')
#     return render(request,'login-otp.html')
# @login_required(login_url='/login/')
# def email_verification(request):
#     if request.method == "POST":
#         u_otp = request.POST['otp']
#         otp = request.session['email_otp']
#         if int(u_otp) == otp:
#            p =  Profile.objects.get(user=request.user)
#            p.email_verified = True
#            p.save()
#            messages.success(request,f'Your email {request.user.email} is verified now')
#            return redirect('/')
#         else:
#             messages.error(request,'Wrong OTP')


#     return render(request,'email-verified.html')

# def forget_password(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         if User.objects.filter(email=email).exists():
#             uid = User.objects.get(email=email)
#             url = f'http://127.0.0.1:8000/change-password/{uid.profile.uuid}'
#             send_mail(
#             'Reset Password',
#             url,
#             settings.EMAIL_HOST_USER,
#             [email],
#             fail_silently=False,
#         )
#             return redirect('/forget-password/done/')
#         else:
#             messages.error(request,'email address is not exist')
#     return render(request,'forget-password.html')

# def change_password(request,uid):
#     try:
#         if Profile.objects.filter(uuid = uid).exists():
#             if request.method == "POST":
#                 pass1 = 'password1'in request.POST and request.POST['password1']
#                 pass2 =  'password2'in request.POST and request.POST['password2']
#                 if pass1 == pass2:
#                     p = Profile.objects.get(uuid=uid)
#                     u = p.user
#                     user = User.objects.get(username=u)
#                     user.password = make_password(pass1)
#                     user.save()
#                     messages.success(request,'Password has been reset successfully')
#                     return redirect('/login/')
#                 else:
#                     return HttpResponse('Two Password did not match')
                
#         else:
#             return HttpResponse('Wrong URL')
#     except:
#         return HttpResponse('Wrong URL')
#     return render(request,'change-password.html')


class BookingHistoryPay(View):
    def get(self, request,*args, **kwargs):
        bookhistories=book_history.objects.filter(user=request.user).order_by('-created')
        payments=payment.objects.filter(user=request.user).order_by('-date')
        testbooking=prescription_book.objects.filter(user=request.user)
        context={
            "bookhistories":bookhistories,
            "payments":payments,
            "testbooking":testbooking,
        }
        return render(request,"booking-history.html",context)
    def post(self, request, *args, **kwargs):
        if request.POST.get("action") == "retreive_data":
            mod = book_history.objects.get(testbooking_id=request.POST.get('id'))
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            tot_amt = int(mod.amount) * 100
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
        if request.POST.get("action") == "payment_canceled":
            mod = book_history.objects.get(testbooking_id=request.POST.get('id'))
            mod.payment_id = None
            mod.payment_status = False
            mod.save()
            to_return = {"valid":True}
        return HttpResponse(json.dumps(to_return), content_type="application/json")
