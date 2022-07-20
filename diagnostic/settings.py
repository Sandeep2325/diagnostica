
from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q6^hx14a=lgi46rai+=20-31f7&-sfp@5tb7i+yf*f%f8xoz-='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["162.240.55.20","127.0.0.1"]
env = environ.Env()


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    "app1",
]
INSTALLED_APPS += ('django_summernote', ) 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'diagnostic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
)
WSGI_APPLICATION = 'diagnostic.wsgi.application'
AUTH_USER_MODEL = 'app1.User'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# DATABASES = {  
#     'default': {  
#         'ENGINE': 'django.db.backends.mysql',  
#         'NAME': 'diagnospan',  
#         'USER': 'root',  
#         'PASSWORD': 'Sandeep@8105',  
#         'HOST': 'localhost',  
#         'PORT': '3306',  
        
#     }  
# } 

DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.mysql',  
        'NAME': 'diagnospan',  
        'USER': 'root',  
        'PASSWORD': 'mySqlServer@#$432',  
        'HOST': 'localhost',  
        'PORT': '3306',   
    }  
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

import os
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
X_FRAME_OPTIONS = 'SAMEORIGIN'
MEDIA_URL = '/photos/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'photos/')
# MEDIA_ROOT = os.path.join(BASE_DIR, 'photos/')
STATIC_ROOT = os.path.join(BASE_DIR, 'app1/static')
STATIC_URL = '/static/'
RAZOR_KEY_ID = "rzp_test_JiD8eNtJ2aNwZr"
RAZOR_KEY_SECRET = "gtukARkLZ5U4Bjo9EfCSWkMf"
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL=FALSE
EMAIL_PORT = 587
EMAIL_HOST_USER = "gowdasandeep8105@gmail.com"
# EMAIL_HOST_PASSWORD = 'Sandeep@1234'
EMAIL_HOST_PASSWORD = 'atkzlpfgzcvpdhai'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SESSION_SAVE_EVERY_REQUEST =True
SWEETIFY_SWEETALERT_LIBRARY = 'sweetalert2'
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Diagnostica Span",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Diagnostica Span",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Diagnostica Span",
    # "site_logo": "jazzmin/img/logo.png",
    "custom_css": "jazzmin/css/custom.css",
    "custom_js": "jazzmin/js/custom.js",
    "order_with_respect_to": ["app1.city","app1.User","app1.aboutspan" "app1.User","app1.category", "app1.test","app1.prescription_book","app1.book_history","app1.healthcheckuppackages","app1.healthpackages","app1.healthcheckuppackages","app1.healthsymptoms","app1.coupons","app1.blogcategory","app1.healthcareblogs","app1.healthcareblogs","app1.subscription","app1.socialmedialinks"],
    "default_icon_parents": "",
    "default_icon_children": "",
    }

