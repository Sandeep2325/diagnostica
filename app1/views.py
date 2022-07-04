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
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import datetime
def Registration(request):
    if request.method == "POST":
        fm = UserRegistrationForm(request.POST)
        up = UserProfileForm(request.POST)
        if fm.is_valid():
            e = fm.cleaned_data['email']
            u = fm.cleaned_data['username']
            p = fm.cleaned_data['password2']
            request.session['email'] = e
            request.session['username'] = u
            request.session['password'] = p
            p_number = fm.cleaned_data['phone_no']
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
    else:
        fm  = UserRegistrationForm()
        up = UserProfileForm()
    context = {'fm':fm,'up':up}
    return render(request,'registration.html',context)


def otpRegistration(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session.get('otp')
        user = request.session['username']
        # hash_pwd=request.session.get('password')
        hash_pwd = make_password(request.session.get('password'))
        p_number = request.session.get('number')
        email_address = request.session.get('email') 

        if int(u_otp) == otp:
            User.objects.create(
                            username = user,
                            email=email_address,
                            phone_no=p_number,
                            password=hash_pwd
            )
            user1=User.objects.get(email=email_address)
            profile.objects.create(
                user=user1,name=user,email=email_address,phone_no=p_number
            ).save()
            # user_instance = User.objects.get(username=user)
            # User.objects.create(
            #                 user = user_instance,phone_number=p_number
            # )
            request.session.delete('otp')
            request.session.delete('user')
            request.session.delete('email')
            request.session.delete('password')
            request.session.delete('phone_number')
            messages.success(request,'Registration Successfully Done !!')
            return redirect('/login/')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'registration-otp.html')
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

def forgotpassword(request):
    if request.method=="POST":
        fm = forgotpasswordform(request.POST)
        if fm.is_valid:
            e = fm.cleaned_data['email']
            # u = fm.cleaned_data['password']
            p = fm.cleaned_data['password2']
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
            return redirect('/registration/otp/')
        else:
            messages.error(request,'Given Email id is wrong')
            
def otpforgotpassword(request):
    if request.method == "POST":
        u_otp = request.POST['otp']
        otp = request.session.get('otp')
        # user = request.session['username']
        # hash_pwd=request.session.get('password')
        hash_pwd = make_password(request.session.get('password'))
        # p_number = request.session.get('number')
        email_address = request.session.get('email') 
        
        if int(u_otp) == otp:
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
            messages.success(request,'Password changed successfully!!')
            return redirect('login')
        else:
            messages.error(request,'Wrong OTP')
    return render(request,'registration-otp.html')      
          
def userLogin(request):
    # try :
    #     if request.session.get('failed') > 2:
    #         return HttpResponse('<h1> You have to wait for 5 minutes to login again</h1>')
    # except:
    #     request.session['failed'] = 0
    #     request.session.set_expiry(100)
    if request.method == "POST":
        username = request.POST['email']
        print(username)
        password = request.POST['password']
        print(password)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Successfull')
            return redirect('/')
        else:
            messages.error(request,'Email or password is wrong')
    return render(request,'login.html')

def home(request):
    print(".....",request.user)
    if request.method =="GET":
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
        }
        return render(request,'home.html',context)
    return render(request,'home.html',context)
def healthcheckupview(request,slug):
    print(slug)
    data=healthcheckuppackages.objects.filter(slug=slug)
    return render(request,'dummy.html',{"data":data})
def healthpackageview(request,slug):
    data=healthpackages.objects.filter(slug=slug)
    return render(request,'',{"data":data})
def healthsymptomview(request,slug):
    data=healthsymptoms.objects.filter(slug=slug)
    return render(request,'',{"data":data})
def healthcareblogsview(request,slug):
    data=healthcareblogs.objects.filter(slug=slug)
    return render(request,'',{"data":data})
def search(request):
    if request.method=="POST":
        searched=request.POST.get('searched')
        venues=test.objects.filter(testt__contains=searched)
        return render(request,"same.html",{'searched':searched,"venues":venues})
    else:
        return render(request,"same.html")
    
def prescriptionbookview(request):
    print(request.FILES)
    fm=prescriptionform()
    if request.method=="POST":
        # others=request.POST.get("myself")
        # print(request.POST)
        # form = prescriptionform(request.POST)
        # form.save()
        # print(request.POST.get("myself"))
        # print(request.POST.get("firstname"))
        # print(request.POST.get("lastname"))
        # print(request.FILES.get("prescription_file"))
        prescription_file=request.FILES.get("prescription_file")
        myself=request.POST.get("myself")
        others=request.POST.get('others')
        others_choice=request.POST.get("others_choice")
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        contact=request.POST.get('contact')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        
        prescription_book(prescription_file=prescription_file,
                          myself=True if myself == "on" else False,
                          others=True if others == "on" else False,
                          others_choice=others_choice,
                          firstname=firstname,
                          lastname=lastname,
                          contact=contact,
                          age=age,
                          gender=gender).save()
        book_history(patient_info="myself" if others==None else "others",
                     booking_type="Prescription",
                     bookingdetails="upload prescription",
                     payment_status=False).save()
        messages.success(request,"Your response is recorded successfully")
        return render(request,"prescriptiontest.html",{"fm":fm})
    else:
        return render(request,"prescriptiontest.html",{"fm":fm})
    
    
def selectedtestview(request):
    print(request.method)
    fm=selectedtestform()
    if request.method=="POST":
        # others=request.POST.get("myself")
        form = selectedtestform(request.POST)
        form.save()
        print(request.POST)
        print(request.POST.getlist("test_name"))
        print(request.POST.get("firstname"))
        print(request.POST.get("lastname"))
        tests=request.POST.getlist("test_name")
        for i in tests:
            item=test.objects.get(id=i)
            cart.objects.create(user=request.user,items=item,categoryy=item.categoryy,price=item.price).save()
        messages.success(request,"Your booking added to cart successfully")
        return render(request,"selectedtest.html",{"fm":fm})
    else:
        return render(request,"selectedtest.html",{"fm":fm})
    
def subscriptionview(request):
    if request.method=="POST":
        form=subscriptionform
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
def destroy(request, slug): 
    print("ok") 
    print(slug)
    employee = healthcheckuppackages.objects.get(slug=slug)  
    employee.delete()  
    return redirect("/")

def coupon(request):
    if request.method=="POST":
        coupon=request.POST.get("coupon")
        try:
            c=coupons.objects.get(couponcode=coupon)
            c.discount
            if datetime.now() > c.enddate:
                messages.error(request,"Coupon Expired")
        except:
            messages.info(request,"Invalid Coupon")
        return redirect("/")
    
@login_required(login_url="login/")    
def bookinghistoryview(request):
    # data=book_history.objects.all()
    data=book_history.objects.filter(user=request.user)
    return render(request,"bookinghistory.html",{"data":data})
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