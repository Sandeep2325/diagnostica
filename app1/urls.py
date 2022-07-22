from django.urls import path,re_path
from .import views
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings 
from wkhtmltopdf.views import PDFTemplateView
"""<a href="{% url 'update' slug=instance.slug %}"> Edit </a>
<a href="{% url 'delete' slug=instance.slug %}"> Delete</a> """
urlpatterns = [
    # path("ip",views.get_client_ip),
    path('',views.home,name="home"),
    path("logout", views.logout_request, name="logout"),
    path("dashboard",views.dashboard),
    path("profile",views.profilee,name="profile"),
    path("aboutus",views.aboutus,name="aboutus"),
    path("contactus",views.contactuss,name="contactus"),
    path("city",views.cityy,name="city"),
    path("faqs",views.faqs,name="faq"),
    path("newsletter",views.newsletter,name="newsletter"),
    path("search",views.search,name="search"),
    path("coupon",views.coupon,name="coupon"),
    path("category",views.categoryy,name="category"),
    path("userinfo",views.userinfo,name="userinfo"),
    path("prescription-upload/",views.prescriptionbookview,name="prescription-upload"),
    path("othersdetail",views.othersdetail,name="othersdetail"),
    path("prescriptionbreak",views.prescriptionbreak,name="prescriptionbreak"),
    path("testselect",views.testselect,name="testselect"),
    path('delete/', views.destroy,name="destroy"),
    path('razorclose/',views.razorpayclose,name="razorpayclose"),
    path("cart",views.cartt,name="cart"),
    path("addtocart/",views.addtocart,name="addtocart"),
    path("healthcheckupadd",views.healthcheckupadd,name="healthcheckupadd"),
    path("bookinghistory/",views.BookingHistoryPay.as_view(),name="booking-history"),
    path("invoice/<str:orderid>/",views.invoice,name="invoice"),
    path('healthcheckup/',views.healthcheckupview, name='Health-checkup'),
    path("packages/",views.hpackagess,name="packages"),
    path('healthcheckups/',views.healthcheckupallview, name='Health-checkups'),
    path('healthpackage/<slug:slug>',views.healthpackageview, name='Health-package'),
    path('healthsymptomview/<slug:slug>/',views.healthsymptomview, name='Health-symptoms'),
    path('blogdetail/<slug:slug>/',views.healthcareblogsview, name='blogsdetail'),
    path('category/<slug:slug>/',views.categoryblog, name='categoryblog'),
    path('registration/',views.Registration, name="Registration"),
    path('registration/otp/',views.otpRegistration, name="otp-Registration"),
    path('resend/',views.resendotp,name="resend"),
    path("book-test-online",views.booktestonline,name="bookonline"),
    path("changepassword",views.changepassword,name="changepassword"),
    path('forgotpassword',views.forgotpassword,name="forgot-password"),
    path("forgotpassword/otp/",views.otpforgotpassword,name="otp-forgotpassword"),
    path('login/',views.userLogin, name="user-login"),
    path("changepasswordotp/",views.changepasswordotp,name="changepasswordotp"),
    path("passwordcheck",views.passwordcheck,name="passwordcheck"),
    path("testdetails",views.testdetails,name="testdetails"),
    # path('login/otp/',views.otpLogin, name="otp-login"),
    # path('logout/',auth_view.LogoutView.as_view(template_name='logout.html')),
    # path('email-verify/', views.email_verification, name="email-verify"),
    # path('forget-password/',views.forget_password,name="forger-password"),
    # path('forget-password/done/',TemplateView.as_view(template_name='forget-password-done.html')),
    # path('change-password/<slug:uid>/',views.change_password,name="change-password"),
    path('paymenthandler/<str:str>/<str:amount>/', views.paymenthandler, name='paymenthandler'),
    path("cartsessiondelete",views.cartsessiondelete,name="cartsessiondelete"),

    path("health-symptoms/<slug:slug>/",views.HealthSymptoms.as_view(),name="health_symptoms"),
    path("couponsessiondelete",views.couponsessiondelete,name='couponsessiondelete'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

