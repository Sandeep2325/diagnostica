# Generated by Django 4.0.5 on 2022-07-19 10:30

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile', verbose_name='Profile photo')),
                ('username', models.CharField(max_length=50, null=True, verbose_name='user name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('phone_no', models.CharField(max_length=10, null=True, unique=True, verbose_name='Mobile number')),
                ('age', models.CharField(blank=True, max_length=50, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'female'), ('o', 'others')], default='choose', max_length=8, null=True)),
                ('is_used', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='aboutspan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description1', models.TextField(blank=True, null=True)),
                ('testedpeople', models.IntegerField(blank=True, null=True)),
                ('verifiedcenter', models.IntegerField(blank=True, null=True)),
                ('cities', models.IntegerField(blank=True, null=True)),
                ('dailyvisits', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'About Span',
            },
        ),
        migrations.CreateModel(
            name='blogcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Blogs Category',
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryy', models.CharField(blank=True, max_length=200, null=True, verbose_name='Category')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Test Category',
            },
        ),
        migrations.CreateModel(
            name='city',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cityname', models.CharField(blank=True, max_length=200, null=True)),
                ('city_icon', models.ImageField(blank=True, null=True, upload_to='photos/icons/')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'City',
            },
        ),
        migrations.CreateModel(
            name='contactus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('subject', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Contact us form',
            },
        ),
        migrations.CreateModel(
            name='coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couponcode', models.CharField(blank=True, max_length=100, null=True, verbose_name='Coupon Code')),
                ('discount', models.CharField(blank=True, max_length=2, null=True, verbose_name='Discount(%)')),
                ('status', models.CharField(choices=[('a', 'Active'), ('i', 'Inactive')], default='a', max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=600, null=True)),
                ('answer', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'FAQ',
            },
        ),
        migrations.CreateModel(
            name='paymentids',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Payment Ids',
            },
        ),
        migrations.CreateModel(
            name='socialmedialinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Social media links',
            },
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Newsletter',
            },
        ),
        migrations.CreateModel(
            name='testimonials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('photo', models.ImageField(blank=True, max_length=500, null=True, upload_to='testimonials', verbose_name='Profile photo')),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Testimonials',
            },
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testt', models.TextField(blank=True, null=True, verbose_name='Test')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
                ('Banglore_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Banglore Price')),
                ('Mumbai_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Mumbai Price')),
                ('bhopal_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Bhopal Price')),
                ('nanded_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Nanded Price')),
                ('pune_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Pune Price')),
                ('barshi_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Barshi Price')),
                ('aurangabad_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Aurangabad Price')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('categoryy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.category')),
            ],
            options={
                'verbose_name_plural': 'Tests',
            },
        ),
        migrations.CreateModel(
            name='prescription_book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique', models.UUIDField(blank=True, null=True)),
                ('prescription_file', models.FileField(blank=True, null=True, upload_to='prescription')),
                ('myself', models.BooleanField(default=False)),
                ('others', models.BooleanField(default=False)),
                ('others_choice', models.CharField(blank=True, choices=[('m', 'Mother'), ('f', 'Father'), ('w', 'Wife'), ('s', 'Son'), ('d', 'Daughter'), ('o', 'Other')], default='', max_length=8, null=True)),
                ('firstname', models.CharField(blank=True, max_length=200, null=True)),
                ('lastname', models.CharField(blank=True, max_length=200, null=True)),
                ('contact', models.CharField(blank=True, max_length=200, null=True)),
                ('age', models.CharField(blank=True, max_length=3, null=True)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Others')], default='', max_length=8, null=True)),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('test_name', models.ManyToManyField(blank=True, to='app1.test')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Test Bookings',
            },
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(blank=True, max_length=50, null=True)),
                ('paymentid', models.CharField(blank=True, max_length=400, null=True)),
                ('transid', models.CharField(blank=True, max_length=400, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, max_length=30, null=True)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Payments History',
            },
        ),
        migrations.CreateModel(
            name='healthsymptoms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('photo', models.ImageField(blank=True, max_length=500, null=True, upload_to='symptoms', verbose_name='Photo')),
                ('symptoms', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('bengaluru_price', models.CharField(blank=True, max_length=10, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('test_name', models.ManyToManyField(to='app1.test')),
            ],
            options={
                'verbose_name_plural': 'Health Symptoms',
            },
        ),
        migrations.CreateModel(
            name='healthpackages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(blank=True, max_length=300, null=True)),
                ('Banglore_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Banglore Price')),
                ('Mumbai_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Mumbai Price')),
                ('bhopal_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Bhopal Price')),
                ('nanded_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Nanded Price')),
                ('pune_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Pune Price')),
                ('barshi_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Barshi Price')),
                ('aurangabad_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Aurangabad Price')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('test_name', models.ManyToManyField(to='app1.test')),
            ],
            options={
                'verbose_name_plural': 'Health Packages',
            },
        ),
        migrations.CreateModel(
            name='healthcheckuppackages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Package Title')),
                ('Banglore_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Banglore Price')),
                ('Mumbai_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Mumbai Price')),
                ('bhopal_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Bhopal Price')),
                ('nanded_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Nanded Price')),
                ('pune_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Pune Price')),
                ('barshi_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Barshi Price')),
                ('aurangabad_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Aurangabad Price')),
                ('dBanglore_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Banglore Discount Price')),
                ('dMumbai_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Mumbai DiscountPrice')),
                ('dbhopal_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Bhopal Discount Price')),
                ('dnanded_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Nanded Discount Price')),
                ('dpune_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Pune Discount Price')),
                ('dbarshi_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Barshi DiscountPrice')),
                ('daurangabad_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Aurangabad DiscountPrice')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Discount(%)')),
                ('slug', models.SlugField(null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('test_name', models.ManyToManyField(to='app1.test')),
            ],
            options={
                'verbose_name_plural': 'Lab Tests',
            },
        ),
        migrations.CreateModel(
            name='healthcareblogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=500, null=True, upload_to='blog', verbose_name='Blog photo')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.blogcategory')),
            ],
            options={
                'verbose_name_plural': 'Blogs',
            },
        ),
        migrations.CreateModel(
            name='cart2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryy', models.CharField(blank=True, max_length=200, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('slug', models.SlugField(null=True, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('items', models.ManyToManyField(to='app1.test')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('device', models.CharField(blank=True, max_length=200, null=True, verbose_name='Device')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('categoryy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.category')),
                ('healthsymptoms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.healthsymptoms', verbose_name='Health Symptoms')),
                ('items', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.test')),
                ('labtest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.healthcheckuppackages')),
                ('packages', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.healthpackages')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='book_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testbooking_id', models.IntegerField(blank=True, null=True)),
                ('patient_info', models.CharField(blank=True, max_length=200, null=True)),
                ('booking_type', models.CharField(blank=True, max_length=200, null=True)),
                ('bookingdetails', models.TextField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(choices=[('p', 'On Process'), ('u', 'updated'), ('t', 'tested')], default='p', max_length=8, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('report', models.FileField(blank=True, null=True, upload_to='report')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Booking Histories',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.city', verbose_name='Locations'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]