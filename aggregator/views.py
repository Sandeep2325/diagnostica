from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from app1.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def loginn(request):
    if request.method=="POST":
        print(request.POST)
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
    return redirect("/aggregator/")

# def dashboardd(request):
#     return render(request,"dashboard.html")

class dashboardd(LoginRequiredMixin,View):
    login_url = '/aggregator/'
    template_name = 'dashboard.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)