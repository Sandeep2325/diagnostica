
from distutils.command.upload import upload
from functools import wraps
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
from shortuuid.django_fields import ShortUUIDField  
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
# from app1.views import html_to_pdf  
from num2words import num2words   
from django.core.files import File   
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
shipping_charges=199
# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
#                                 message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

# class users(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
#     email_verified = models.BooleanField(default=False)
#     uuid = models.UUIDField(default=uuid.uuid4,editable=False)
class city(models.Model):
    cityname=models.CharField(max_length=200,null=True,blank=True)
    city_icon= models.ImageField(upload_to = "photos/icons/", null=True, blank=True)
    active=models.BooleanField(default=True,verbose_name="Is Active")
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.cityname
    class Meta:
        verbose_name_plural="City"
        verbose_name="City"
class aboutspan(models.Model):
    description1=models.TextField(null=True,blank=True)
    testedpeople=models.IntegerField(null=True,blank=True)  
    verifiedcenter=models.IntegerField(null=True,blank=True) 
    cities=models.IntegerField(null=True,blank=True) 
    dailyvisits=models.IntegerField(null=True,blank=True) 
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return str(self.description1)[0:15]
    class Meta:
        verbose_name_plural = "About Span"
        verbose_name = "About Span"
        
GENDER_CHOICES = (
  
    ("m","Male"),
    ("f","female"),
    ("o","others")
    )

class User(AbstractUser,PermissionsMixin):
    photo=models.ImageField(upload_to='profile',verbose_name="Profile photo", null=True, blank=True)
    username = models.CharField(
        max_length=50, blank=False, null=True,verbose_name="user name")
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=13, null=True, unique=True,verbose_name="Mobile number")
    location=models.ForeignKey(city, verbose_name=_("Locations"), null=True,blank=True,on_delete=models.CASCADE)
    age=models.CharField(max_length=50,blank=True,null=True)
    address=models.TextField(null=True,blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=8,
        default="", null=True,blank=True
    )
    aggregator = models.BooleanField(default=False,)
    is_used = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_no']
    def __str__(self):
        return "{}".format(str(self.first_name))
    class Meta:
        verbose_name_plural = "Registered Users"
class category(models.Model):
    categoryy=models.CharField(max_length=200,null=True,blank=True,verbose_name="Category")
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.categoryy
    class Meta:
        verbose_name_plural = "Test Category"
        verbose_name = "Test Category"
class test(models.Model):
    testt=models.TextField(null=True,blank=True,verbose_name="Test")
    testcode=models.CharField(max_length=50,null=True,blank=True,verbose_name="Test Code")
    description=models.TextField(null=True,blank=True)
    categoryy=models.ForeignKey(category,null=True,blank=True,on_delete=models.CASCADE,verbose_name="Category")
    is_active=models.BooleanField(default=True,verbose_name="Is Active?")
    # price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    Banglore_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    Mumbai_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai Price")
    bhopal_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Bhopal Price")
    nanded_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Nanded Price")
    pune_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Pune Price")
    barshi_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Barshi Price")
    aurangabad_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Aurangabad Price")
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # slug = models.SlugField(null=True, unique=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        if self.testt==None:
            return "Tests"
        else:
            return self.testt
    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.testt)
    #     return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Tests"
        verbose_name="Master Test"
STATUS_CHOICES1 = (
    ('m', 'Mother'),
    ('f', 'Father'),
    ('w','Wife'),
    ('s', 'Son'),
    ('d',"Daughter"),
    ('o',"Other")
)    
STATUS_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('o','Others')
)   
# class prescription_book(models.Model):
#     unique=models.UUIDField(null=True,blank=True)
#     user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
#     prescription_file=models.FileField(upload_to="prescription",null=True,blank=True)
#     test_name=models.ManyToManyField(test,blank=True)
#     price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
#     myself=models.BooleanField(default=False)
#     others=models.BooleanField(default=False)
#     others_choice = models.CharField(
#         choices=STATUS_CHOICES1,
#         max_length=8,
#         default="", null=True,blank=True
#     )
#     firstname=models.CharField(max_length=200,null=True,blank=True)
#     lastname=models.CharField(max_length=200,null=True,blank=True)
#     contact=models.CharField(max_length=200,null=True,blank=True)
#     age=models.CharField(max_length=3,null=True,blank=True)
#     gender = models.CharField(
#         choices=STATUS_CHOICES,
#         max_length=8,
#         default="", null=True,blank=True
#     )
#     location=models.CharField(max_length=100,null=True,blank=True)
#     address=models.TextField(null=True,blank=True)
#     created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True,null=True, blank=True)

#     def __str__(self):
#         return "Prescription booking1"
#     class Meta:
#         default_permissions = ('add',)
#         verbose_name_plural="Prescription Bookings1" 
        
TIME_CHOICES = (
    ("1","7:00AM-11:00AM"),
    ("2","11:00AM-3:00PM"),
    ("3","3:00PM-6:00PM")
)  
class testbook(models.Model):
    bookingid=models.CharField(max_length=20,null=True,blank=True)
    unique=models.UUIDField(null=True,blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    tests=models.TextField(null=True,blank=True)
    # prescription_file=models.FileField(upload_to="prescription",null=True,blank=True)
    # test_name=models.ManyToManyField(test,blank=True)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    myself=models.BooleanField(default=False)
    others=models.BooleanField(default=False)
    others_choice = models.CharField(
        choices=STATUS_CHOICES1,
        max_length=8,
        default="", null=True,blank=True
    )
    timeslot = models.CharField(
        choices=TIME_CHOICES,
        max_length=20,
        default="", null=True,blank=True,verbose_name="Time Slot"
    )
    date=models.DateField(null=True,blank=True)
    payment_status=models.BooleanField(default=False)
    firstname=models.CharField(max_length=200,null=True,blank=True)
    lastname=models.CharField(max_length=200,null=True,blank=True)
    contact=models.CharField(max_length=200,null=True,blank=True)
    age=models.CharField(max_length=3,null=True,blank=True)
    gender = models.CharField(
        choices=STATUS_CHOICES,
        max_length=8,
        default="", null=True,blank=True
    )
    comments=models.TextField(null=True,blank=True,verbose_name="Comments")
    locationn=models.ForeignKey(city,null=True,blank=True,on_delete=models.CASCADE,verbose_name="Location")
    pincode=models.CharField(max_length=100,null=True,blank=True,verbose_name="Pincode")
    address=models.TextField(null=True,blank=True)
    report=models.FileField(upload_to="report",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return "Test booking"
    class Meta:
        verbose_name_plural="Test Bookings" 
        verbose_name="Test Bookings"
@receiver(post_save, sender=testbook)
def reportresponse(sender, instance, **kwargs):
    
    # if (instance.payment_status== True) and (bool(instance.report) == True):
    #     send_mail(str("Tests Report | Dignostica Span"),
    #               (f"Hi {instance.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {instance.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDignostica Span"),
    #               settings.EMAIL_HOST_USER,
    #               [instance.user.email],
    #               fail_silently=False)
    # if (instance.payment_status== True) and (bool(instance.report) == True):
    #     # print("sent")
    #     send_mail(str("DIAGNOSTICA SPAN TEST REPORT"),
    #               ("Dear Customer,\n Your Report is Added to your dashboard,Please Checkit out"),
    #               settings.EMAIL_HOST_USER,
    #               [instance.user.email],
    #               fail_silently=False)    
    ...            
PAYMENT_METHOD = (
    ("1","Cash on Collection"),
    ("2","Online"),
)  
class Prescriptionbook1(models.Model):
    bookingid=models.CharField(max_length=20,null=True,blank=True)
    unique=models.UUIDField(null=True,blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    prescription_file=models.FileField(upload_to="prescription",null=True,blank=True)
    test_name=models.ManyToManyField(test,blank=True)
    # price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    myself=models.BooleanField(default=False)
    others=models.BooleanField(default=False)
    others_choice = models.CharField(
        choices=STATUS_CHOICES1,
        max_length=8,
        default="", null=True,blank=True
    )
    date=models.DateField(null=True,blank=True)
    timeslot = models.CharField(
        choices=TIME_CHOICES,
        max_length=20,
        default="", null=True,blank=True,verbose_name="Time Slot"
    )
    
    payment_status=models.BooleanField(default=False)
    firstname=models.CharField(max_length=200,null=True,blank=True)
    lastname=models.CharField(max_length=200,null=True,blank=True)
    contact=models.CharField(max_length=200,null=True,blank=True)
    age=models.CharField(max_length=3,null=True,blank=True)
    gender = models.CharField(
        choices=STATUS_CHOICES,
        max_length=8,
        default="", null=True,blank=True
    )
    price=models.CharField(max_length=20,null=True,blank=True,verbose_name="Price(Rs)",help_text=mark_safe(_('<p style="color:green">Rs 199 Will be Added As Sample Collection charges</p>')))
    location=models.CharField(max_length=100,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    pincode=models.CharField(max_length=100,null=True,blank=True,verbose_name="Pincode")
    paymentmethod=models.CharField(
        choices=PAYMENT_METHOD,
        max_length=100,
        default="", null=True,blank=True,verbose_name="Payment Method"
    )
    coupon=models.ForeignKey("coupons",null=True,blank=True,on_delete=models.CASCADE,help_text=mark_safe(_('<small style="color:red">*Coupon Should be Apply Only Once"</small>')))
    comments=models.TextField(null=True,blank=True,verbose_name="Comments")
    report=models.FileField(upload_to="report",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    # @property
    # def payment(self):
    #     if self.payment_status== True:
    #         return book_history.objects.filter(uni=self.bookingid).update(payment_status=True)
            # return self.test_name.all().count()
    
    def __str__(self):
        return "Prescription booking"
    class Meta:
        verbose_name_plural="Prescription Bookings"
        verbose_name="Prescription Bookings"
    # def save(self,*args,**kwargs):
    #     if (self.payment_status== True) and (bool(self.report) == True):
    #         print("--------in")
    #         send_mail(str("Tests Report | Dignostica Span"),
    #                   (f"Hi {self.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {instance.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDignostica Span"),
    #                   settings.EMAIL_HOST_USER,
    #                   [self.user.email],
    #                   fail_silently=False)
    #     return super().save(self,*args,**kwargs)
 
@receiver(post_save, sender=Prescriptionbook1)
def testbookings(sender, instance, **kwargs):
    # print("qwertyu")
    if instance.price==None:
        a=[]
        for i in instance.test_name.all():
            if instance.location=="Bangalore":
                a.append(i.Banglore_price)

            elif instance.location=="Mumbai":
                a.append(i.Mumbai_price)

            elif instance.location=="Bhophal":
                a.append(i.bhopal_price)

            elif instance.location=="Nanded":
                a.append(i.nanded_price)

            elif instance.location=="Pune":
                a.append(i.pune_price)

            elif instance.location=="Barshi":
                a.append(i.barshi_price)

            elif instance.location=="Aurangabad":
                a.append(i.aurangabad_price)

        if sum(a)!=0:
            book_history.objects.filter(uni=instance.bookingid).update(amount=sum(a)+shipping_charges)
            Prescriptionbook1.objects.filter(bookingid=instance.bookingid).update(price=sum(a)+shipping_charges)
        else:
            book_history.objects.filter(uni=instance.bookingid).update(amount=None)
            Prescriptionbook1.objects.filter(bookingid=instance.bookingid).update(price=None)
        
    if instance.payment_status== True:
        book_history.objects.filter(uni=instance.bookingid).update(payment_status=True)
        
    # print("-------",instance.coupon.couponcode)    
    if instance.coupon:
        print("---------",instance.coupon.couponcode) 
        try:
            from datetime import datetime,timezone 
            c=coupons.objects.get(couponcode=instance.coupon.couponcode,status="active")
            couponcount=couponredeem.objects.filter(coupon=instance.coupon).count()
            presc=Prescriptionbook1.objects.get(bookingid=instance.bookingid)
            if presc.coupon==None:
                if datetime.now(timezone.utc)>c.startdate:
                    if datetime.now(timezone.utc)<c.enddate:
                        if c.cityy.filter(cityname=instance.location).exists():
                            # if c.limit!=0 or c.limit>0:
                            try:
                                if couponcount<c.limit:
                                    c.discount
                                    # print("=====",c.discount)
                                    # print(float(float(instance.price)-199))
                                    discount=(float(float(instance.price)-shipping_charges)*(int(c.discount)/100))
                                    # print("###########",discount)
                                    totall=(float(float(instance.price)-shipping_charges)-int(discount))+shipping_charges
                                    # print(totall)
                                    # instance.price=totall
                                    Prescriptionbook1.objects.filter(bookingid=instance.bookingid).update(price=totall)
                                    book_history.objects.filter(uni=instance.bookingid).update(amount=totall)
                                    couponredeem.objects.create(user=instance.user,booking_id=instance.bookingid,coupon=instance.coupon.couponcode,discountpercen=c.discount,discountamount=discount,actualamount=float(instance.price)-shipping_charges).save()
                                else:
                                    instance.coupon=None
                            except:
                                c.discount
                                # print("=====",c.discount)
                                print(float(float(instance.price)-shipping_charges))
                                discount=(float(float(instance.price)-shipping_charges)*(int(c.discount)/100))
                                # print("###########",discount)
                                totall=(float(float(instance.price)-shipping_charges)-int(discount))+shipping_charges
                                # print(totall)
                                # instance.price=totall
                                Prescriptionbook1.objects.filter(bookingid=instance.bookingid).update(price=totall)
                                book_history.objects.filter(uni=instance.bookingid).update(amount=totall)
                                couponredeem.objects.create(user=instance.user,booking_id=instance.bookingid,coupon=instance.coupon.couponcode,discountpercen=c.discount,discountamount=discount,actualamount=float(instance.price)-shipping_charges).save()

                                    # raise ValidationError("Invalid Coupon")
                                    # return JsonResponse({"message":False})
                            # else:
                            #     instance.coupon=None
                            #     # raise ValidationError("Invalid Coupon")
                            #     # return JsonResponse({"message":False})
                        else:
                            instance.coupon=None
                            # raise ValidationError("Invalid Coupon")
                            # return JsonResponse({"message":False})
                    else:
                        instance.coupon=None
                        # raise ValidationError("Invalid Coupon")
                        # return JsonResponse({"message":False})

                else:
                    instance.coupon=None
                    # raise ValidationError("Invalid Coupon")
                    # return JsonResponse({"message":False})
            else:
                    instance.coupon=None
                    # raise ValidationError("Invalid Coupon")
                    # return JsonResponse({"message":False})
        except Exception as e:
            # print("-----------",e)
            # c=coupons.objects.get(couponcode=instance.coupon.couponcode) 
            instance.coupon=None
            # raise ValidationError("Invalid Coupon")
            # return JsonResponse({"message":False})
    # if (instance.payment_status== True) and (bool(instance.report) == True):
    #     send_mail(str("Tests Report | Dignostica Span"),
    #               (f"Hi {instance.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {instance.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDignostica Span"),
    #               settings.EMAIL_HOST_USER,
    #               [instance.user.email],
    #               fail_silently=False)
    # if (instance.test_name.first()!=None) and (bool(instance.prescription_file)==True and bool(instance.report) == False): 
            
    #         send_mail(str("Booking Confirmation | Dignostica Span" ),
    #                     (f"Hi {instance.user.first_name} ,\nThis mail is regarding the booking id: {instance.bookingid}, recently booked by you, \nWe have reviewed your prescription and have added the tests for your testing Please check your dashboard,\nKindly visit your dashboard to review it and pay the mentioned amount to confirm the booking.\nHave a speedy and healthy recovery.\nThank you,\nDignostica Span"),
    #                     settings.EMAIL_HOST_USER,
    #                     [instance.user.email],
    #                     fail_silently=False)
m2m_changed.connect(testbookings, sender=Prescriptionbook1.test_name.through)
# post_save.disconnect(testbookings, sender=Prescriptionbook1) 
class healthcheckuppackages(models.Model):
    package_title=models.CharField(max_length=200,null=True,blank=True,verbose_name="Test Name")
    test_name=models.ManyToManyField(test,blank=True)
    Banglore_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    Mumbai_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai Price")
    bhopal_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Bhopal Price")
    nanded_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Nanded Price")
    pune_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Pune Price")
    barshi_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Barshi Price")
    aurangabad_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Aurangabad Price")

    dBanglore_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    dMumbai_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai DiscountPrice")
    dbhopal_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Bhopal Discount Price")
    dnanded_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Nanded Discount Price")
    dpune_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Pune Discount Price")
    dbarshi_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Barshi DiscountPrice")
    daurangabad_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Aurangabad DiscountPrice")
    
    description=models.TextField(null=True,blank=True,verbose_name="Description")
    discount=models.DecimalField(max_digits=5, decimal_places=2, null=True,blank=True,verbose_name='Discount(%)', validators=[
        MinValueValidator(1), MaxValueValidator(99)])
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.package_title
    class Meta:
        verbose_name_plural = "Popular Tests"
        verbose_name="Popular Tests"
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.package_title)
        return super().save(*args, **kwargs)
    @property
    def testcount(self):
        return self.test_name.all().count()
   
class healthpackages(models.Model):
    package_name=models.CharField(max_length=300,null=True,blank=True)
    # location=models.ForeignKey(city,null=True,on_delete=models.CASCADE,verbose_name="Location")
    test_name=models.ManyToManyField(test,blank=True)
    Banglore_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    Mumbai_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai Price")
    bhopal_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Bhopal Price")
    nanded_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Nanded Price")
    pune_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Pune Price")
    barshi_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Barshi Price")
    aurangabad_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Aurangabad Price")
    discounted_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Discounted Price")
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.package_name
    class Meta:
        verbose_name_plural = "Health Packages"
        verbose_name = "Health Packages"
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(uuid.uuid4())
        return super().save(*args, **kwargs)
    @property
    def testcount(self):
        return self.test_name.all().count()   
class healthsymptoms(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    photo=models.ImageField(upload_to='symptoms',max_length=500, verbose_name="Photo", null=True, blank=True)
    symptoms=models.TextField(null=True,blank=True)
    test_name=models.ManyToManyField(test,blank=True)
    slug = models.SlugField(null=True, unique=True)
    Banglore_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    Mumbai_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai Price")
    bhopal_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Bhopal Price")
    nanded_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Nanded Price")
    pune_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Pune Price")
    barshi_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Barshi Price")
    aurangabad_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Aurangabad Price")
    discounted_price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Price")
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Life Style Assesments"
        verbose_name = "Life Style Assesments"
    # def save(self, *args, **kwargs):  # new
    #     a=[]
    #     for i in self.test_name.all():
    #         if i!=None:
    #             a.append(i.Banglore_price)
    #         else:
    #             a.append(0)
    #     print(a)
    #     self.Banglore_price=sum(a)
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     return super().save(*args, **kwargs)
# @receiver(post_save, sender=healthsymptoms)
# def lifestyleprice(sender, instance, **kwargs):
#     # print(instance)
#     a=[]
#     for i in instance.test_name.all():
#         if i.Banglore_price is not None:
#             #print(i.Banglore_price)
#             a.append(i.Banglore_price)
#         else:
#             a.append(0)
#     healthsymptoms.objects.filter(id=instance.id).update(Banglore_price=sum(a))
# m2m_changed.connect(lifestyleprice, sender=healthsymptoms.test_name.through)
# post_save.disconnect(lifestyleprice, sender=healthsymptoms)  
class healthcareblogs(models.Model):
    image=models.ImageField(upload_to='blog',max_length=500, verbose_name="Blog photo", null=True, blank=True)
    title=models.CharField(max_length=300,blank=True,null=True)
    description=models.TextField(null=True,blank=True)
    category=models.ForeignKey("blogcategory",null=True,blank=True,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField( unique=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Blogs"
        verbose_name = "Blogs"
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
class blogcategory(models.Model):
    category=models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField( unique=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    def __str__(self):
        return self.category
    class Meta:
        verbose_name_plural="Blogs Category"
        verbose_name="Blogs Category"
class testimonials(models.Model):
    username=models.CharField(max_length=200,null=True,blank=True)
    photo=models.ImageField(upload_to='testimonials',max_length=500, verbose_name="Profile photo", null=True, blank=True)
    description=models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.username
    class Meta:
        verbose_name_plural = "Testimonials"
        verbose_name = "Testimonials"
        
class cart(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    items=models.ForeignKey(test,null=True,blank=True,on_delete=models.CASCADE)
    labtest=models.ForeignKey(healthcheckuppackages,null=True,blank=True,on_delete=models.CASCADE)
    packages=models.ForeignKey(healthpackages,null=True,blank=True,on_delete=models.CASCADE)
    categoryy=models.ForeignKey(category,null=True,blank=True,on_delete=models.CASCADE)
    healthsymptoms = models.ForeignKey(healthsymptoms, verbose_name=_("Health Symptoms"), on_delete=models.CASCADE, null=True, blank=True)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    device = models.CharField(_("Device"), max_length=200,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
class invoicee(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=200,null=True,blank=True)
    items=models.ForeignKey(test,null=True,blank=True,on_delete=models.CASCADE)
    labtest=models.ForeignKey(healthcheckuppackages,null=True,blank=True,on_delete=models.CASCADE)
    packages=models.ForeignKey(healthpackages,null=True,blank=True,on_delete=models.CASCADE)
    healthsymptoms = models.ForeignKey(healthsymptoms, verbose_name=_("Health Symptoms"), on_delete=models.CASCADE, null=True, blank=True)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    file=models.FileField(upload_to='invoice',max_length=500, verbose_name="Invoice File", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    def __str__(self):
        return self.order_id
    class Meta:
        verbose_name_plural = "Invoice"
        verbose_name = "Invoice"
    # def save(self, *args, **kwargs):
    #     order=book_history.objects.get(payment_id=self.order_id)
    #     payments=payment.objects.get(transid=self.order_id)
    #     try:
    #         testbooking=Prescriptionbook1.objects.get(bookingid=order.uni)
    #     except:
    #         testbooking=testbook.objects.get(bookingid=order.uni)
            
    #     invoic=invoicee.objects.filter(order_id=self.order_id)
    #     amount=payments.amount
    #     amount1=num2words(int(float(amount)), lang = 'en_IN')
    #     c=amount1.replace(",","")
    #     try:
    #         coupoonn=couponredeem.objects.get(order_id=self.order_id)
    #         couponamount=coupoonn.actualamount
    #         couponamount=num2words(int(float(couponamount)), lang = 'en_IN')
    #         a=couponamount.replace(",","")
    #         amount=num2words(int(float(amount)), lang = 'en_IN')
    #         b=amount.replace(",","")
    #         context_dict={
            
    #         "order":order,
    #         "payments":payments,
    #         "testbooking":testbooking,
    #         "tests":invoic,
    #         "coupon":coupoonn,
    #         "couponamount":a,
    #         "amount":b
    #             }

    #     except:
    #         # coupoonn=couponredeem.objects.get(order_id=orderid)
    #         context_dict={
    #         "order":order,
    #         "payments":payments,
    #         "testbooking":testbooking,
    #         "tests":invoic,
    #         # "couponamount":num2words(int(couponamount), to = 'ordinal'),
    #         "amount":c
    #             }
    #     template_name='invoice2.html'
    #     pdf = html_to_pdf(template_name,context_dict)
    #     receipt_file = BytesIO(pdf.content)
    #     filee = invoicee.objects.get(order_id=self.order_id)
    #     filee.file = File(receipt_file, "invoice2.pdf")
    #     filee.save()

# @receiver(post_save, sender=invoicee)
# def invoiceefile(sender, instance, **kwargs):
#     order=book_history.objects.get(payment_id=instance.order_id)
#     payments=payment.objects.get(transid=instance.order_id)
#     try:
#         testbooking=Prescriptionbook1.objects.get(bookingid=order.uni)
#     except:
#         testbooking=testbook.objects.get(bookingid=order.uni)
#     invoic=invoicee.objects.filter(order_id=instance.order_id)
#     amount=payments.amount
#     amount1=num2words(int(float(amount)), lang = 'en_IN')
#     c=amount1.replace(",","")
#     try:
#         coupoonn=couponredeem.objects.get(order_id=instance.order_id)
#         couponamount=coupoonn.actualamount
#         couponamount=num2words(int(float(couponamount)), lang = 'en_IN')
#         a=couponamount.replace(",","")
#         amount=num2words(int(float(amount)), lang = 'en_IN')
#         b=amount.replace(",","")
#         context_dict={
        
#         "order":order,
#         "payments":payments,
#         "testbooking":testbooking,
#         "tests":invoic,
#         "coupon":coupoonn,
#         "couponamount":a,
#         "amount":b
#             }
        
#     except:
#         # coupoonn=couponredeem.objects.get(order_id=orderid)
#         context_dict={
#         "order":order,
#         "payments":payments,
#         "testbooking":testbooking,
#         "tests":invoic,
#         # "couponamount":num2words(int(couponamount), to = 'ordinal'),
#         "amount":c
#             }
#     template_name='invoice2.html'
#     pdf = html_to_pdf(template_name,context_dict)
#     receipt_file = BytesIO(pdf.content)
#     filee = invoicee.objects.get(order_id=instance.order_id)
#     filee.file = File(receipt_file, "invoice2.pdf")
#     filee.save()
    
STATUS=[
    ('p','On Process'),
    ('u',"updated"),
    ('t',"tested")
]  

class book_history(models.Model):
    testbooking_id=models.IntegerField(null=True,blank=True)
    bookingid = ShortUUIDField(
        length=16,
        max_length=40,
        prefix="DP",
        verbose_name="Booking Id",
        null=True, blank=True
    )
    uni=models.CharField( max_length=50,null=True,blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    patient_info=models.CharField(max_length=200,null=True,blank=True)
    booking_type=models.CharField(max_length=200,null=True,blank=True)
    bookingdetails=models.TextField(null=True,blank=True)
    amount=models.CharField(max_length=20,null=True,blank=True)
    payment_id=models.CharField(max_length=500,null=True,blank=True,verbose_name="Order Id")
    status = models.CharField(
        choices=STATUS,
        max_length=8,
        default="p", null=True
    )
    payment_status=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    report=models.FileField(upload_to="report",null=True,blank=True)
    def __str__(self):
        return "Book History"
    class Meta:
        verbose_name_plural="Booking Histories"
        verbose_name="Booking Histories"
   
@receiver(post_save, sender=book_history)
def reportresponse(sender, instance, **kwargs):
    if (instance.payment_status== True) and (bool(instance.report) == True):
        print("sent")
        send_mail(str("DIAGNOSTICA SPAN TEST REPORT"),
                  ("Dear Customer,\n Your Report is Added to your dashboard,Please Checkit out"),
                  settings.EMAIL_HOST_USER,
                  [instance.user.email],
                  fail_silently=False)
class payment(models.Model):
    booking_id=models.CharField(max_length=50,null=True,blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    paymentid=models.CharField(max_length=400,null=True,blank=True,verbose_name="Payment Id")
    transid=models.CharField(max_length=400,null=True,blank=True,verbose_name="Order Id")
    # signatureid=models.CharField(max_length=500,null=True,blank=True,verbose_name="signature Id Id"),
    date=models.DateTimeField(auto_now_add=True,max_length=30,null=True,blank=True)
    amount=models.CharField(max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.paymentid

    class Meta:
        verbose_name_plural="Payments History"
        verbose_name="Payments History"
class subscription(models.Model):
    email=models.EmailField(max_length=255,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural="Subscriptions"
        verbose_name="Subscriptions"
class socialmedialinks(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    url=models.URLField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return "Social Media Links"
    class Meta:
        verbose_name_plural="Social media links"
        verbose_name="Social media links"
SELECT_CHOICES=[
    ("active","Active"),
    ("inactive","Inactive")
]
class coupons(models.Model):
    couponcode=models.CharField(max_length=15,null=True,blank=True,verbose_name="Coupon Code",help_text=_('Enter maximum 15 characters only'),unique=True)
    discount=models.CharField(max_length=2,null=True,blank=True,verbose_name="Discount(%)")
    limit=models.PositiveIntegerField(null=True,blank=True,verbose_name="Usage Limit")
    cityy=models.ManyToManyField(city,blank=True,verbose_name="City")
    
    # cityy=models.ForeignKey(city,null=True,blank=True,on_delete=models.CASCADE,verbose_name="City")
    status = models.CharField(
        choices=SELECT_CHOICES,
        max_length=100,
        default="active", null=True
    )
    startdate=models.DateTimeField(null=True, blank=True)
    enddate=models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.couponcode
    
    def clean(self):
        try:
            if self.startdate > self.enddate:
                raise ValidationError("Start Date should be less than End Date")
        except:
            pass
    class Meta:
        verbose_name_plural="Coupons"
        verbose_name="Coupons"

class faq(models.Model):
    question=models.CharField(max_length=600,null=True,blank=True)
    answer=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural="FAQ"
        verbose_name="FAQ"

class contactus(models.Model):
    fullname=models.CharField(max_length=200,blank=True,null=True)
    email=models.EmailField(max_length=255,null=True,blank=True)
    phone=models.CharField(max_length=13,null=True,blank=True)
    subject=models.TextField(null=True,blank=True)
    message=models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.fullname
    class Meta:
        verbose_name_plural="Contact us form"
        verbose_name="Contact us form"

# class paymentids(models.Model):
#     orderid=models.CharField(max_length=200,null=True,blank=True),
#     paymentid=models.CharField(max_length=200,null=True,blank=True),
#     signatureid=models.CharField(max_length=500,null=True,blank=True),
    
#     def __str__(self):
#         return self.paymentid
#     class Meta:
#         verbose_name_plural="Payment Ids"
class couponredeem(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    booking_id=models.CharField(max_length=50,null=True,blank=True)
    order_id=models.CharField(max_length=200,null=True,blank=True)
    coupon=models.CharField(max_length=200,null=True,blank=True)
    discountpercen=models.CharField(max_length=200,null=True,blank=True,verbose_name="Discount(%)")
    discountamount=models.CharField(max_length=20,null=True,blank=True,verbose_name="Discounted Price(₹)")
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    actualamount=models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return self.coupon
    class Meta:
        verbose_name_plural="Redeemed Coupons"
        verbose_name="Redeemed Coupons"
class requestcall(models.Model):
    firstname=models.CharField(max_length=100,null=True,blank=True,verbose_name="First Name")
    lastname=models.CharField(max_length=100,null=True,blank=True,verbose_name="First Name")
    phone=models.CharField(max_length=14,null=True,blank=True,verbose_name="First Name")
    email=models.EmailField(max_length=255,null=True,blank=True)
    tests=models.ForeignKey(test,null=True,blank=True,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.firstname
    class Meta:
        verbose_name_plural="Call Back Requests"
        verbose_name="Call Back Requests"
    

    
