from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from app1.models import User,aggregatorbookings,test,book_history,city
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.views import View
import shortuuid
import re
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def loginn(request):
    if request.method=="POST":
        username=request.POST.get("email")
        password=request.POST.get("password")
        try:
            User.objects.get(email=username)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.aggregator:
                    login(request,user)  
                    return redirect(reverse('aggregator-dashboardd'))
                else:
                    messages.error(request,'Invalid credentials')
            else:
                messages.error(request,'Invalid credentials')
        except:
            messages.error(request,'Invalid credentials')
    return render(request,"aggregatorlogin.html")

def aggregatorlogout_request(request):
    logout(request)
    return redirect("/aggregator/login")
class dashboardd(LoginRequiredMixin,View):
    login_url = '/aggregator/login'
    template_name = 'dashboard.html'
    
    def get(self, request, *args, **kwargs):
        # print("----",request.GET.get("searched"))
        # data=aggregatorbookings.objects.filter(user=request.user).order_by("-created")
        searched_name = request.GET.get("searched")
        fromdate=request.GET.get("fromdate")
        todate=request.GET.get("todate")
        if searched_name != None:
            data=aggregatorbookings.objects.filter(user=request.user,bookingid__icontains=searched_name).order_by("-created")
        elif fromdate != None and todate != None:
            try:
                data=aggregatorbookings.objects.filter(user=request.user,created__range=[fromdate, todate]).order_by("-created")
            except:
                data=aggregatorbookings.objects.filter(user=request.user).order_by("-created")
        else:
            data=aggregatorbookings.objects.filter(user=request.user).order_by("-created")
        return render(request, self.template_name,{"data":data,"count":data.count()})

    # def post(self, request, *args, **kwargs):
    #     if request.POST.get("action")=="testdetails":
    #         return render(request,"testdetails.html")
    #     else:
    #         searched_name = request.POST.get("searched")
    #         fromdate=request.POST.get("fromdate")
    #         todate=request.POST.get("todate")
    #         if searched_name != None:
    #             data=aggregatorbookings.objects.filter(user=request.user,bookingid__icontains=searched_name).order_by("-created")
    #         elif fromdate != None and todate != None:
    #             try:
    #                 data=aggregatorbookings.objects.filter(user=request.user,created__range=[fromdate, todate]).order_by("-created")
    #             except:
    #                 data=aggregatorbookings.objects.filter(user=request.user).order_by("-created")
    #         # return redirect(data)
    #         # return reverse("aggregator-dashboardd")
    #         # return HttpResponseRedirect(reverse('aggregator-dashboardd'))
    #         return render(request, self.template_name,{"data":data,"count":data.count()})
class detailtest(LoginRequiredMixin,View):
    login_url = '/aggregator/login'
    template_name = 'testdetails.html'
    def get(self,request,bookingid,*args, **kwargs):
        data=aggregatorbookings.objects.get(bookingid=bookingid)
        total=[]
        for i in data.test_name.all():
            total.append(float(i.Banglore_price))
        return render(request,"testdetails.html",{"data":data,"total":sum(total)})
class addform(LoginRequiredMixin,View):
    login_url = '/aggregator/login'
    template_name = 'addform.html'
    def get(self, request, *args, **kwargs):
        data=test.objects.all()
        citi=city.objects.filter(active=True)
        return render(request, self.template_name,{"data":data,"city":citi})
    def post(self, request, *args, **kwargs):
        cit=request.POST.get("cityy")
        ids=request.POST.getlist("selected")
        s = shortuuid.ShortUUID(alphabet="0123456789")
        bid = s.random(length=5)
        book=book_history.objects.all().order_by("-created")[0:1]
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
        location=city.objects.get(id=int(cit))
        aggr=aggregatorbookings.objects.create(user=request.user,bookingid=bookingid)
        book_history(
            user=request.user,
            uni=bookingid,
            bookingid=bookingid,
            # patient_info="myself" if others==None else "others",
                    booking_type="Aggregator",
                    # bookingdetails="upload prescription",
                    payment_status=False).save()
        price=[]
        for i in ids:
            a=test.objects.get(id=int(i))
            price.append(int(a.Banglore_price))
            # print(aggr)
            aggr.test_name.add(a)
            # print(i,aggr)
        aggr.location=location
        aggr.price=sum(price)
        aggr.save()
        # template_name = 'dashboard.html'
        return redirect("aggregator-dashboardd")
class search(LoginRequiredMixin,View):
    login_url = '/aggregator/login'
    template_name = 'addform.html'
    def get(self, request, *args, **kwargs):
        searched_name = request.POST.get("searched")
        data=aggregatorbookings.objects.filter(bookingid__icontains=searched_name)
        return render(request, self.template_name,{"data":data})
def aggregatortests(request):
    if request.method=="POST":
        id=request.POST["id"]
        try:
            tests=aggregatorbookings.objects.get(bookingid__icontains=id)
            strr=[]
            for i in tests.test_name.all():
                di={}
                di["test"]=(i.testt)
                strr.append(di)
            return JsonResponse({"message":strr})
        except Exception as e:
            print("----------",e)
            return JsonResponse({"message":False})
class aggregatorprofile(LoginRequiredMixin,View):
    login_url = '/aggregator/login'
    template_name = 'aggreprofile.html'
    
    def get(self, request, *args, **kwargs):
        totalorders=aggregatorbookings.objects.filter(user=request.user).count()
        paid=aggregatorbookings.objects.filter(user=request.user,payment_status=True).count()
        unpaid=aggregatorbookings.objects.filter(user=request.user,payment_status=False)
        pending=[]
        for i in unpaid:
            pending.append(int(i.price))
        context={
            "totalorders":totalorders,
            "paid":paid,
            "pending":sum(pending),
            "pending_no":unpaid.count()
        }
        return render(request,self.template_name,context)
class changepassword(LoginRequiredMixin,View):
    login_url = '/aggregator/login'
    template_name = 'changepasswordd.html'
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    def post(self,request,*args,**kargs):
        curpassword=request.POST["oldpassword"]
        newpassword=request.POST["newpassword"]
        connewpassword=request.POST["confirmnewpassword"]
        try:
            a=authenticate(request,username=request.user.email,password=curpassword)
            # print(a)
            if newpassword==newpassword:
                a.password=make_password(connewpassword)
                a.save()
                messages.success(request,"Password Changed Successfully! Please Login Again")
                return render(request,self.template_name)
            else:
                messages.warning(request,"Confirm Password didn't match with new password")
                return render(request,self.template_name)
        except:
            messages.warning(request,"Invalid Password")
        return render(request,self.template_name)