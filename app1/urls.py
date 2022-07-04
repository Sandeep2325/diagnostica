from django.urls import path
from .import views,payments
from django.contrib.auth import views as auth_view
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings 

"""<a href="{% url 'update' slug=instance.slug %}"> Edit </a>
<a href="{% url 'delete' slug=instance.slug %}"> Delete</a> """
urlpatterns = [
    path('',views.home,name="home"),
    path("prescription/",views.prescriptionbookview,name="prescriptiontest"),
    path("selectedtest/",views.selectedtestview,name="selectedtest"),
    path('delete/<int:id>', views.destroy,name="destroy"),
    path("bookinghistory/",views.bookinghistoryview,name="booking-history"),
    path('healthcheckup/<slug:slug>/',views.healthcheckupview, name='Health-checkup'),
    path('healthpackage/<slug:slug>/',views.healthpackageview, name='Healt-package'),
    path('healthsymptomview/<slug:slug>/',views.healthsymptomview, name='Health-symptoms'),
    path('healthcareblogsview/<slug:slug>/',views.healthcareblogsview, name='Health-blogs'),
    path('registration/',views.Registration, name="Registration"),
    path('registration/otp/',views.otpRegistration, name="otp-Registration"),
    path('resend/',views.resendotp,name="resend"),
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
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)