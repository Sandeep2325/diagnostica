from django.urls import path,re_path
from .import views,payments
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings 

"""<a href="{% url 'update' slug=instance.slug %}"> Edit </a>
<a href="{% url 'delete' slug=instance.slug %}"> Delete</a> """
urlpatterns = [
    # path("ip",views.get_client_ip),
    
    path('',views.home,name="home"),
    path("logout", views.logout_request, name="logout"),
    path("dashboard",views.dashboard),
    path("profile",views.profilee,name="profile"),
    path("city",views.cityy),
    path("search",views.search,name="search"),
    path("prescription-upload/",views.prescriptionbookview,name="prescription-upload"),
    path("testselect/",views.testselect,name="testselect"),
    path('delete/', views.destroy,name="destroy"),
    path("cart",views.cartt,name="cart"),
    path("addtocart/",views.addtocart,name="addtocart"),
    path("bookinghistory/",views.bookinghistoryview,name="booking-history"),
    path('healthcheckup/<slug:slug>/',views.healthcheckupview, name='Health-checkup'),
    path('healthpackage/<slug:slug>/',views.healthpackageview, name='Healt-package'),
    path('healthsymptomview/<slug:slug>/',views.healthsymptomview, name='Health-symptoms'),
    path('healthcareblogsview/<slug:slug>/',views.healthcareblogsview, name='Health-blogs'),
    path('registration/',views.Registration, name="Registration"),
    path('registration/otp/',views.otpRegistration, name="otp-Registration"),
    path('resend/',views.resendotp,name="resend"),
    path("book-test-online",views.booktestonline,name="bookonline"),
    path('forgotpassword',views.forgotpassword,name="forgot-password"),
    path("forgotpassword/otp/",views.otpforgotpassword,name="otp-forgotpassword"),
    path('login/',views.userLogin, name="user-login"),
    # path('login/otp/',views.otpLogin, name="otp-login"),
    # path('logout/',auth_view.LogoutView.as_view(template_name='logout.html')),
    # path('email-verify/', views.email_verification, name="email-verify"),
    # path('forget-password/',views.forget_password,name="forger-password"),
    # path('forget-password/done/',TemplateView.as_view(template_name='forget-password-done.html')),
    # path('change-password/<slug:uid>/',views.change_password,name="change-password"),
    path('payment/', payments.payment, name='index'),
    path('paymenthandler/', payments.paymenthandler, name='paymenthandler'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)