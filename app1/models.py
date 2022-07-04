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
# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
#                                 message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

# class users(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=17,validators=[phone_regex],unique=True)
#     email_verified = models.BooleanField(default=False)
#     uuid = models.UUIDField(default=uuid.uuid4,editable=False)
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
class User(AbstractUser,PermissionsMixin):
    username = models.CharField(
        max_length=50, blank=False, null=True,verbose_name="Full name")
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=10, null=True, unique=True)
    otp = models.IntegerField(default=False)
    is_used = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_no']
    def __str__(self):
        return "{}".format(str(self.username))
    
GENDER_CHOICES = (
    ("m","Male"),
    ("f","female"),
    ) 
class profile(models.Model):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='Profile',max_length=500, verbose_name="Profile photo", null=True, blank=True)
    name=models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=255,null=True,blank=True)
    phone_no = models.CharField(max_length=10, null=True, unique=True,blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=8,
        default="choose", null=True,blank=True
    )
    location=models.CharField(max_length=200,null=True,blank=True)
    dob=models.CharField(max_length=50,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    slug = models.SlugField(null=True, unique=True)
    def __str__(self):
        return str(self.user.username)
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "User Profiles"
class category(models.Model):
    categoryy=models.CharField(max_length=200,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.categoryy
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.categoryy)
        return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "  Test Category"
class test(models.Model):
    testt=models.CharField(max_length=200,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    categoryy=models.ForeignKey(category,null=True,blank=True,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits = 10,decimal_places = 2,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField(null=True, unique=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.testt
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.testt)
        return super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "   Tests"
STATUS_CHOICES1 = (
    ('m', 'Mother'),
    ('f', 'Father'),
    ('s', 'Son'),
    ('d',"Daughter"),
    ('o',"Other")
)    
STATUS_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
)   
class prescription_book(models.Model):
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
    # slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.test_name)
    #     return super().save(*args, **kwargs)
    def __str__(self):
        return "Prescription booking"
    class Meta:
        verbose_name_plural="Test Bookings"
# class selectedtest_book(models.Model):
#     user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
#     test_name=models.ManyToManyField(test)
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
#     # slug = models.SlugField(null=True, unique=True)
#     created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
#     updated = models.DateTimeField(auto_now=True,null=True, blank=True)
#     # def save(self, *args, **kwargs):  # new
#     #     if not self.slug:
#     #         self.slug = slugify(self.test_name)
#     #     return super().save(*args, **kwargs)
#     def __str__(self):
#         return "Test booking"
#     class Meta:
#         verbose_name_plural="Tests Bookings"
class healthcheckuppackages(models.Model):
    package_title=models.CharField(max_length=200,null=True,blank=True,verbose_name="Package Title")
    test_name=models.ManyToManyField(test)
    test_nos=models.CharField(max_length=100,null=True,blank=True,verbose_name="No of test")
    description=models.TextField(null=True,blank=True,verbose_name="Description")
    actual_price=models.IntegerField(null=True,blank=True,verbose_name="Actual Price(₹)")
    discount=models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Discount(%)', validators=[
        MinValueValidator(1), MaxValueValidator(99)])
    discounted_price=models.IntegerField(null=True,blank=True,verbose_name="Discounted Price(₹)")
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.package_title
    class Meta:
        verbose_name_plural = " Health Checkup"
    def save(self, *args, **kwargs):  # new
        discount_price=self.actual_price*(self.discount/100)
        self.test_nos=self.test_name.all().count()
        self.discounted_price=self.actual_price-discount_price
        if not self.slug:
            self.slug = slugify(self.package_title)
        return super().save(*args, **kwargs)
class healthpackages(models.Model):
    package_name=models.CharField(max_length=300,null=True,blank=True)
    test_name=models.ManyToManyField(test)
    actual_price=models.IntegerField(null=True,blank=True)
    discount=models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name='Discount(%)', validators=[
        MinValueValidator(1), MaxValueValidator(99)])
    discounted_price=models.IntegerField(null=True,blank=True)
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.package_name
    class Meta:
        verbose_name_plural = " Health Packages"
    def save(self, *args, **kwargs):  # new
        discount_price=self.actual_price*(self.discount/100)
        self.discounted_price=self.actual_price-discount_price
        if not self.slug:
            self.slug = slugify(self.package_name)
        return super().save(*args, **kwargs)
class healthsymptoms(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    symptoms=models.TextField(null=True,blank=True)
    test_name=models.ManyToManyField(test)
    slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = " Health Symptoms"
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
class healthcareblogs(models.Model):
    image=models.ImageField(upload_to='blog',max_length=500, verbose_name="Blog photo", null=True, blank=True)
    title=models.CharField(max_length=300,blank=True,null=True)
    description=models.TextField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    slug = models.SlugField( unique=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = " Health care blogs"
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
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
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # patient_info=models.ForeignKey(cart2,null=True,blank=True,on_delete=models.CASCADE)
    patient_info=models.CharField(max_length=200,null=True,blank=True)
    booking_type=models.CharField(max_length=200,null=True,blank=True)
    bookingdetails=models.TextField(null=True,blank=True)
    amount=models.IntegerField(null=True,blank=True)
    status = models.CharField(
        choices=STATUS,
        max_length=8,
        default="p", null=True
    )
    payment_status=models.BooleanField(default=False)
    # slug = models.SlugField(null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    report=models.FileField(upload_to="report",null=True,blank=True)
    # def save(self, *args, **kwargs):  # new
    #     if not self.slug:
    #         self.slug = slugify(self.patient_info)
    #     return super().save(*args, **kwargs)
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
        verbose_name_plural="Subscriptions"
class socialmedialinks(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True)
    url=models.URLField(null=True,blank=True)
    def __str__(self):
        return "Social Media Links"
    class Meta:
        verbose_name_plural="Social media links"
class coupons(models.Model):
    couponcode=models.CharField(max_length=100,null=True,blank=True,verbose_name="Coupon Code")
    discount=models.CharField(max_length=2,null=True,blank=True,verbose_name="Discount(%)")
    startdate=models.DateTimeField(null=True,blank=True,verbose_name="Start Date")
    enddate=models.DateTimeField(null=True,blank=True,verbose_name="Start Date")
    
    def __str__(self):
        return self.couponcode
    class Meta:
        verbose_name_plural="Coupons"
        
