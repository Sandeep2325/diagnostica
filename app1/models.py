
from distutils.command.upload import upload
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
    location=models.ForeignKey(city, verbose_name=_("Locations"), null=True,blank=True,on_delete=models.SET_NULL)
    age=models.CharField(max_length=50,blank=True,null=True)
    address=models.TextField(null=True,blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=8,
        default="", null=True,blank=True
    )
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
class prescription_book(models.Model):
    unique=models.UUIDField(null=True,blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    prescription_file=models.FileField(upload_to="prescription",null=True,blank=True)
    test_name=models.ManyToManyField(test,blank=True)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    myself=models.BooleanField(default=False)
    others=models.BooleanField(default=False)
    others_choice = models.CharField(
        choices=STATUS_CHOICES1,
        max_length=8,
        default="", null=True,blank=True
    )
    firstname=models.CharField(max_length=200,null=True,blank=True)
    lastname=models.CharField(max_length=200,null=True,blank=True)
    contact=models.CharField(max_length=200,null=True,blank=True)
    age=models.CharField(max_length=3,null=True,blank=True)
    gender = models.CharField(
        choices=STATUS_CHOICES,
        max_length=8,
        default="", null=True,blank=True
    )
    location=models.CharField(max_length=100,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return "Prescription booking1"
    class Meta:
        verbose_name_plural="Prescription Bookings1" 
        
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
    location=models.CharField(max_length=100,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    report=models.FileField(upload_to="report",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return "Test booking"
    class Meta:
        verbose_name_plural="Test Bookings" 
    
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
    price=models.CharField(max_length=20,null=True,blank=True)
    location=models.CharField(max_length=100,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    report=models.FileField(upload_to="report",null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    def __str__(self):
        return "Prescription booking"
    class Meta:
        verbose_name_plural="Prescription Bookings"

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
    # print(sender)
    # print(sum(a))
          
    book_history.objects.filter(uni=instance.bookingid).update(amount=sum(a))
    # instance.price=sum(a)
    
    Prescriptionbook1.objects.filter(bookingid=instance.bookingid).update(price=sum(a))
    # if (instance.payment_status== True) and (bool(instance.report) == True):
    #     send_mail(str("Tests Report | Dignostica Span"),
    #               (f"Hi {instance.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {instance.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDignostica Span"),
    #               settings.EMAIL_HOST_USER,
    #               [instance.user.email],
    #               fail_silently=False)
    if (instance.test_name.first()!=None) and (bool(instance.prescription_file)==True and bool(instance.report) == False): 
            # print("sent")
            # link=request.build_absolute_uri('/bookinghistory/')
            send_mail(str("Booking Confirmation | Dignostica Span" ),
                        (f"Hi {instance.user.first_name} ,\nThis mail is regarding the booking id: {instance.bookingid}, recently booked by you, \nWe have reviewed your prescription and have added the tests for your testing Please check your dashboard,\nKindly visit your dashboard to review it and pay the mentioned amount to confirm the booking.\nHave a speedy and healthy recovery.\nThank you,\nDignostica Span"),
                        settings.EMAIL_HOST_USER,
                        [instance.user.email],
                        fail_silently=False)
m2m_changed.connect(testbookings, sender=Prescriptionbook1.test_name.through)
post_save.disconnect(testbookings, sender=Prescriptionbook1) 

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

    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.package_name
    class Meta:
        verbose_name_plural = "Health Packages"
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
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Life Style Assesments"
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
        
class cart(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    items=models.ForeignKey(test,null=True,blank=True,on_delete=models.CASCADE)
    labtest=models.ForeignKey(healthcheckuppackages,null=True,blank=True,on_delete=models.CASCADE)
    packages=models.ForeignKey(healthpackages,null=True,blank=True,on_delete=models.CASCADE)
    categoryy=models.ForeignKey(category,null=True,blank=True,on_delete=models.SET_NULL)
    healthsymptoms = models.ForeignKey(healthsymptoms, verbose_name=_("Health Symptoms"), on_delete=models.SET_NULL, null=True, blank=True)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    device = models.CharField(_("Device"), max_length=200,null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

class invoicee(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=200,null=True,blank=True)
    items=models.ForeignKey(test,null=True,blank=True,on_delete=models.CASCADE)
    labtest=models.ForeignKey(healthcheckuppackages,null=True,blank=True,on_delete=models.CASCADE)
    packages=models.ForeignKey(healthpackages,null=True,blank=True,on_delete=models.CASCADE)
    healthsymptoms = models.ForeignKey(healthsymptoms, verbose_name=_("Health Symptoms"), on_delete=models.SET_NULL, null=True, blank=True)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
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
class subscription(models.Model):
    email=models.EmailField(max_length=255,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural="Subscriptions"
class socialmedialinks(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    url=models.URLField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return "Social Media Links"
    class Meta:
        verbose_name_plural="Social media links"
SELECT_CHOICES=[
    ("a","Active"),
    ("i","Inactive")
]
class coupons(models.Model):
    couponcode=models.CharField(max_length=100,null=True,blank=True,verbose_name="Coupon Code")
    discount=models.CharField(max_length=2,null=True,blank=True,verbose_name="Discount(%)")
    # cityy=models.ForeignKey(city,null=True,blank=True,on_delete=models.CASCADE,verbose_name="City")
    status = models.CharField(
        choices=SELECT_CHOICES,
        max_length=100,
        default="a", null=True
    )
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.couponcode
    class Meta:
        verbose_name_plural="Coupons"

class faq(models.Model):
    question=models.CharField(max_length=600,null=True,blank=True)
    answer=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural="FAQ"

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

# class paymentids(models.Model):
#     orderid=models.CharField(max_length=200,null=True,blank=True),
#     paymentid=models.CharField(max_length=200,null=True,blank=True),
#     signatureid=models.CharField(max_length=500,null=True,blank=True),
    
#     def __str__(self):
#         return self.paymentid
#     class Meta:
#         verbose_name_plural="Payment Ids"
class couponredeem(models.Model):
    order_id=models.CharField(max_length=200,null=True,blank=True)
    coupon=models.CharField(max_length=200,null=True,blank=True)
    discountpercen=models.CharField(max_length=200,null=True,blank=True,verbose_name="Discount(%)")
    discountamount=models.CharField(max_length=20,null=True,blank=True,verbose_name="Discounted Price(₹)")
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    actualamount=models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
        return self.order_id
    class Meta:
        verbose_name_plural="Redeemed Coupons"
class requestcall(models.Model):
    firstname=models.CharField(max_length=100,null=True,blank=True,verbose_name="First Name")
    lastname=models.CharField(max_length=100,null=True,blank=True,verbose_name="First Name")
    phone=models.CharField(max_length=14,null=True,blank=True,verbose_name="First Name")
    email=models.EmailField(max_length=255,null=True,blank=True)
    tests=models.ForeignKey(test,null=True,blank=True,on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.firstname
    class Meta:
        verbose_name_plural="Call Back Requests"
    

    
