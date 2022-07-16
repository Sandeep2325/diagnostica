import email
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver
# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
#                                 message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

# class users(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
#     email_verified = models.BooleanField(default=False)
#     uuid = models.UUIDField(default=uuid.uuid4,editable=False)
class city(models.Model):
    cityname=models.CharField(max_length=200,null=True,blank=True)
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
    photo=models.ImageField(upload_to='Profile',max_length=500, verbose_name="Profile photo", null=True, blank=True)
    username = models.CharField(
        max_length=50, blank=False, null=True,verbose_name="user name")
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=10, null=True, unique=True,verbose_name="Mobile number")
    location=models.CharField(max_length=200,null=True,blank=True)
    age=models.CharField(max_length=50,blank=True,null=True)
    address=models.TextField(null=True,blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=8,
        default="choose", null=True,blank=True
    )
    is_used = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_no']
    def __str__(self):
        return "{}".format(str(self.username))
    
# class profile(models.Model):
#     user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
#     photo=models.ImageField(upload_to='Profile',max_length=500, verbose_name="Profile photo", null=True, blank=True)
#     name=models.CharField(max_length=200,null=True,blank=True)
#     email = models.EmailField(max_length=255,null=True,blank=True)
#     phone_no = models.CharField(max_length=10, null=True, unique=True,blank=True)
#     gender = models.CharField(
#         choices=GENDER_CHOICES,
#         max_length=8,
#         default="choose", null=True,blank=True
#     )
#     location=models.CharField(max_length=200,null=True,blank=True)
#     dob=models.CharField(max_length=50,blank=True,null=True)
#     created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True,null=True, blank=True)
#     slug = models.SlugField(null=True, unique=True)
#     def __str__(self):
#         return str(self.user.username)
#     def save(self, *args, **kwargs):  # new
#         if not self.slug:
#             self.slug = slugify(self.name)
#         return super().save(*args, **kwargs)
#     class Meta:
#         verbose_name_plural = "User Profiles"
class category(models.Model):
    categoryy=models.CharField(max_length=200,null=True,blank=True,verbose_name="Category")
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.categoryy
    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.categoryy)
    #     return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Test Category"
class test(models.Model):
    testt=models.CharField(max_length=200,null=True,blank=True,verbose_name="Test")
    description=models.TextField(null=True,blank=True)
    categoryy=models.ForeignKey(category,null=True,blank=True,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True,verbose_name="Is Active?")
    # price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    pricel1=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    pricel2=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai Price")
    pricel3=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Chennai Price")
    pricel4=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Hyderabad Price")
    pricel5=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Delhi Price")
    pricel6=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Kolkata Price")
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # slug = models.SlugField(null=True, unique=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
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
)   
class prescription_book(models.Model):
    unique=models.UUIDField(null=True,blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    prescription_file=models.FileField(upload_to="prescription",null=True,blank=True)
    test_name=models.ManyToManyField(test,blank=True)
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
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return "Prescription booking"
    class Meta:
        verbose_name_plural="Test Bookings" 
        
@receiver(post_save, sender=prescription_book)
def testbookings(sender, instance, **kwargs):
    a=[]
    for i in instance.test_name.all():
        if instance.location=="Bangalore":
            a.append(i.pricel1)
        elif instance.location=="Chennai":
            a.append(i.pricel2)
        elif instance.location=="Mumbai":
            a.append(i.pricel3)
        elif instance.location=="Delhi":
            a.append(i.pricel3)
    book_history.objects.filter(testbooking_id=instance.id).update(amount=sum(a))
    # print(bool(instance.prescription_file))
    if (instance.test_name.first()!=None) and (bool(instance.prescription_file)==True): 
            print("sent")
            send_mail(str("Hello"),
                        ("Tests are added as per your Prescription please check"),
                        settings.EMAIL_HOST_USER,
                        [instance.user.email],
                        fail_silently=False)
m2m_changed.connect(testbookings, sender=prescription_book.test_name.through)
class healthcheckuppackages(models.Model):
    package_title=models.CharField(max_length=200,null=True,blank=True,verbose_name="Package Title")
    test_name=models.ManyToManyField(test)
    # location=models.ForeignKey(city,null=True,on_delete=models.CASCADE,verbose_name="Location")
    # test_nos=models.CharField(max_length=100,null=True,blank=True,verbose_name="No of test")
    pricel1=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    pricel2=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Chennai Price")
    pricel3=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai Price")
    pricel4=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Delhi Price")
    # pricel5=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Delhi Price")
    # pricel6=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Kolkata Price")
    dpricel1=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Discounted Price")
    dpricel2=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Chennai Discounted Price")
    dpricel3=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai DiscountedPrice")
    dpricel4=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Delhi Discounted Price")
    # dpricel5=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Delhi DiscountedPrice")
    # dpricel6=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Kolkata Discounted Price")
    description=models.TextField(null=True,blank=True,verbose_name="Description")
    # actual_price=models.IntegerField(null=True,blank=True,verbose_name="Actual Price(₹)")
    discount=models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Discount(%)', validators=[
        MinValueValidator(1), MaxValueValidator(99)])
    # discounted_price=models.IntegerField(null=True,blank=True,verbose_name="Discounted Price(₹)")
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.package_title
    class Meta:
        verbose_name_plural = "Lab Tests"
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
    test_name=models.ManyToManyField(test)
    description=models.TextField(null=True,blank=True,verbose_name="Description")
    pricel1=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Banglore Price")
    pricel2=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Mumbai Price")
    pricel3=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Chennai Price")
    pricel4=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Hyderabad Price")
    pricel5=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Delhi Price")
    pricel6=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True,verbose_name="Kolkata Price")

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
    test_name=models.ManyToManyField(test)
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Health Symptoms"
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
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
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    
class cart2(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    items=models.ManyToManyField(test)
    categoryy=models.CharField(max_length=200,null=True,blank=True)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
STATUS=[
    ('p','On Process'),
    ('u',"updated"),
    ('t',"tested")
]    
class book_history(models.Model):
    testbooking_id=models.IntegerField(null=True,blank=True)
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    patient_info=models.CharField(max_length=200,null=True,blank=True)
    booking_type=models.CharField(max_length=200,null=True,blank=True)
    bookingdetails=models.TextField(null=True,blank=True)
    amount=models.IntegerField(null=True,blank=True)
    payment_id=models.CharField(max_length=500,null=True,blank=True)
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
class subscription(models.Model):
    email=models.EmailField(max_length=255,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name_plural="Newsletter"
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
    def __str__(self):
        return self.fullname
    class Meta:
        verbose_name_plural="Contact us form"
class payment(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    paymentid=models.CharField(max_length=400,null=True,blank=True)
    transid=models.CharField(max_length=400,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True,max_length=30,null=True,blank=True)
    amount=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.paymentid

    class Meta:
        verbose_name_plural="Payments History"
class paymentids(models.Model):
    orderid=models.CharField(max_length=200,null=True,blank=True),
    paymentid=models.CharField(max_length=200,null=True,blank=True),
    signatureid=models.CharField(max_length=500,null=True,blank=True),
    
    def __str__(self):
        return self.paymentid
    class Meta:
        verbose_name_plural="Payment Ids"
# class dummycart(models.Model):
#     name=models.CharField(max_length=500,null=True,blank=True)
#     category=models.CharField(max_length=500,null=True,blank=True)
#     price=models.CharField(max_length=10,null=True,blank=True)
