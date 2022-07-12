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
import datetime
import uuid
import json
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import HttpResponseRedirect
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
    # print(context)
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
    #   newpassword=request.POST["password"]
      conpassword=request.POST["confirmpassword"]
      request.session["ppassword"]=password 
    #   request.session["newpassword"]=newpassword 
      request.session["conpassword"]=conpassword 
      otp = random.randint(1000,9999)
      email_address = request.user.email
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
      return redirect('/forgotpassword/otp/')
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
            # messages.success(request,'Password changed successfully!!')
            return redirect('user-login')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'otpforgot.html')    
     
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
            # user_instance = User.objects.get(username=user)
            # User.objects.create(
            #                 user = user_instance,phone_number=p_number
            # )
            request.session.delete('otp')
            request.session.delete('email')
            request.session.delete('password')
            # messages.success(request,'Password changed successfully!!')
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
def profilee(request):
    profile=User.objects.get(email=request.user.email)
    context={
        "profile":profile,
    }
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        gender=request.POST["gender"]
        location=request.POST["location"]
        dob=request.POST["date"]
        address=request.POST["address"]
        print(request.POST)
        User.objects.filter(email=request.user.email).update(username=name,
                                                             email=email,
                                                             phone_no=phone,
                                                             gender=gender,
                                                             location=location,
                                                             dob=dob,
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
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,'Email or password is wrong')
    return render(request,'login.html')
@login_required(login_url="login/")  
def booktestonline(request):
    return render(request,"book-test-online.html")
from django.contrib.auth import logout
def logout_request(request):
    logout(request)
    print(request.session.get("city"))
    
    request.session.delete("city")
    print(request.session.get("city"))
    return redirect("/")
def newsletter(request):
    if request.method=="POST":
        email=request.POST["email"]
        subscription.objects.create(email=email).save()
        return JsonResponse({"message":True,"email":email})
    # return render(request,"footer.html")
def home(request):
    print(request.session.get("city"))
    c=request.session.get("city")
    print(".....",request.user)
    if request.method =="GET":
        cit=city.objects.all()
        tests=test.objects.all()
        healthcheckup=healthcheckuppackages.objects.all()
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
        print(c)
        return render(request,'home.html',context)
    
    
    testt=request.POST["selectbookhelp"]
    tes=test.objects.get(id=testt)
    firtname=request.POST["firstname"]
    lastname=request.POST["lastname"]
    phone=request.POST["phone"]
    email=request.POST["email"]
    print(testt)
    if c == "Bangalore":
        cart.objects.create(user=request.user,items=tes,categoryy=tes.categoryy,price=tes.pricel1).save()
    elif c == "Chennai":
        cart.objects.create(user=request.user,items=tes,categoryy=tes.categoryy,price=tes.pricel2).save()
    elif c == "Mumbai":
        cart.objects.create(user=request.user,items=tes,categoryy=tes.categoryy,price=tes.pricel3).save()
    elif c == "Delhi":
        cart.objects.create(user=request.user,items=tes,categoryy=tes.categoryy,price=tes.pricel3).save()
     
    cit=city.objects.all()
    tests=test.objects.all()
    healthcheckup=healthcheckuppackages.objects.all()
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
    return HttpResponseRedirect(reverse("cart"))

def healthcheckupview(request,slug):
    c=request.session.get("city")
    city="Hyderabad"
    data=healthcheckuppackages.objects.filter(slug=slug)
    context={
        "data":data,
        "city":city
    }
    return render(request,'dummy.html',context)
def hpackagess(request):
    packages=healthpackages.objects.all()
    city=request.session.get("city")
    context={
        "packages":packages,
        "city":city,
    }
    return render(request,'healthpackages.html',context)

# @login_required(login_url="login/") 
def healthpackageview(request,slug):
    if request.user.is_anonymous:
        # return redirect("user-login")
        return HttpResponseRedirect(reverse("user-login"))
    else:
        
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
        request.session["order_id"]=razorpay_order['id']
        request.session['amount']=amount
        razorpay_order_id = razorpay_order['id']

        
        
        callback_url = callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        print("okkk")
        return render(request,'packagedetail.html',context)
    
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
@login_required(login_url="login/")   
def prescriptionbookview(request):
    c=request.session.get("city")
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
        return render(request,"uploadprescriptions.html",{"fm":fm})
    else:
        return render(request,"uploadprescriptions.html",{"fm":fm})
    
@login_required(login_url="login/")  
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
        test_name=request.POST.getlist("test_name")
        myself=request.POST.get("myself")
        others=request.POST.get('others')
        others_choice=request.POST.get("others_choice")
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        contact=request.POST.get('contact')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
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
import razorpay
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url="login/")    
def cartt(request):
    print(request.POST)
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
        global uniquee
        uniquee = uuid.uuid4()
        print(firstname)
        print(others)
        print(others_choice)
        print(gender)
        print(firstname)
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
        for j in data:
            item=test.objects.get(id=j.items.id)
            a.test_name.add(item)
        data2=prescription_book.objects.get(unique=uniquee)
        data1=cart.objects.filter(user=request.user)
        a=[]
        for i in data:
            a.append(i.price)
        def testname():
            return ", ".join([
                test.testt for test in data2.test_name.all()
            ])
        bookhistory=book_history(
            user=request.user,
            testbooking_id=data2.id,
            patient_info="myself" if others==None else "others",
                     booking_type="Selected test",
                     bookingdetails=testname(),
                     amount=sum(a),
                     payment_id=request.session.get("order_id"),
                     payment_status=False).save()
        request.session.delete("order_id")
        
        return JsonResponse({"message":True})
    
    data=cart.objects.filter(user=request.user)
    p = Paginator(data, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    a=[]
    for i in data:
        a.append(i.price)
    context={
        "data":data,
        "subtotal":sum(a),
        'page_obj': page_obj
    }
    currency = 'INR'
    amount=int(sum(a))
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
    request.session['amount']=amount
    razorpay_order_id = razorpay_order['id']
    request.build_absolute_uri('/bands/?print=true')
    # print("----------",request.user.email,amount)
    callback_url = request.build_absolute_uri('/paymenthandler/{}/{}/'.format(request.user.email,amount))
    # callback_url = 'http://127.0.0.1:8000/paymenthandler/{}/{}/'.format(request.user.email,amount)
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request,"mycart.html",context)

@csrf_exempt
def paymenthandler(request,str,amount):
    if request.method =="POST":
        print(str)
        usr=User.objects.get(email=str)
        paymentid=request.POST["razorpay_payment_id"]
        transid=request.POST["razorpay_order_id"]
        print(amount)
        cart.objects.filter(user=usr).delete()
        payment.objects.create(user=usr,paymentid=paymentid,transid=transid,amount=amount).save()
        history=book_history.objects.get(payment_id=transid)
        history.payment_status=True
        history.save()
        request.session.delete("amount")
        return HttpResponse("Payment Successfull")
        # return redirect("bookinghistory/")
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
def addtocart(request):
    if request.method=="POST":
        tests=test.objects.all()
        pk=request.POST["pk"]
        # print(pk)
        # print(request.method)
      
        item=test.objects.get(id=pk)
        data=cart.objects.filter(user=request.user,items=item)
        print(data)
        if data.exists():
            return JsonResponse({"message":False})
        cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.pricel1).save()
        messages.success(request,"add to cart")
        print("success")
        return JsonResponse({"message":True})
        # return JsonResponse({"message":"success"})
def categoryy(request):
    print(request.method)
    if request.method=="POST":
        pk=request.POST["pk"]
        b=[]
        tests=test.objects.filter(categoryy__id=pk).values("id","testt","description","pricel1")
        for tesst in tests:
            tesst['pricel1'] = str(tesst['pricel1'])
            print(tesst)
            b.append(tesst)
            # a["test"]=tesst.testt
            # a["description"]=tesst.description
            # a["pricel1"]=tesst.pricel1
            # b.append(a)
        return JsonResponse(b,safe=False)
    
def search(request):
    if request.method=="POST":
        searched=request.GET.get('searched')
        searched=request.POST["searched"]
        tcategories=category.objects.all()
        b=[]
        a={}
        tests=test.objects.filter(testt__icontains=searched)
        for tesst in tests:
            a["id"]=tesst.id
            a["testt"]=tesst.testt
            a["description"]=tesst.description
            a["pricel1"]=str(tesst.pricel1)
            b.append(a)
        print(b)
        return JsonResponse(b,safe=False)
        return render(request,"choose-test-list.html",context)
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
        # return JsonResponse({"message": "Wrong request"})
def coupon(request):
    if request.method=="POST":
        print(request.POST)
        coupon=request.POST.get("coupon")
        total=request.POST.get("total")
        try:
            c=coupons.objects.get(couponcode=coupon)
            c.discount
            discount=(float(total)*(int(c.discount)/100))
            # print(t)
            totall=float(total)-int(discount)
            return JsonResponse({"message":True,"total":totall})
        except:
            print("Invalid")
            return JsonResponse({"message":False})
        # return redirect("/")
def contactuss(request):
    if request.method=="POST":
        name=request.POST["name"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        subject=request.POST["subject"]
        message=request.POST["message"]
        contactus.objects.create(fullname=name,email=email,phone=phone,subject=subject,message=message).save()
        messages.success(request,"Your response submitted successfully")
        return render(request,"contactus.html")
    return render(request,"contactus.html")       
@login_required(login_url="login/")    
def bookinghistoryview(request):
    # data=book_history.objects.all()
    print(request.user)
    bookhistories=book_history.objects.filter(user=request.user).order_by('-created')
    payments=payment.objects.filter(user=request.user).order_by('-date')
    testbooking=prescription_book.objects.filter(user=request.user)
    context={
        "bookhistories":bookhistories,
        "payments":payments,
        "testbooking":testbooking,
    }
    
    return render(request,"booking-history.html",context)
def faqs(request):
    faqss=faq.objects.all()
    return render(request,"faq.html",{"faqs":faqss})
from django.http import FileResponse
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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
    
    # payment=payment.objects.get(id=order_id)
    # print(order.order_payment_id)
    # data=cart2.objects.filter(order_id=order_id)
    # total_amount=[]
    # for i in data:
    #     total_amount.append(float(i.price))
    # amount=sum(total_amount)   
    # gst= amount*0.18
    # deliver_charge=(amount+gst)*0.04
    # grand_total=order.total_price
    # paymentid=payment.objects.get(order_id=order_id)
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