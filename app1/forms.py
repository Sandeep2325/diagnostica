from dataclasses import fields
from django import forms
from django.forms import ModelForm
from app1.models import *
import datetime
from django.contrib.auth.password_validation import validate_password
class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()
def email_exist(value):
    if User.objects.filter(email=value).exists():
        return forms.ValidationError("Profile with this Email Address already exists")

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(validators=[email_exist])
    password = forms.CharField(required=True, validators=[validate_password])
    password2 = forms.CharField(required=True, validators=[validate_password])
    class Meta:
        model = User
        fields  =['username','email','phone_no',"password","password2"]

class UserProfileForm(forms.ModelForm):
    # phone_number = forms.CharField(max_length=17,validators=[phone_regex])
    
    class Meta:
        model = User
        fields =['username','email','phone_no']
class forgotpasswordform(forms.Form):
    email = forms.EmailField(validators=[email_exist])
    password = forms.CharField(required=True, validators=[validate_password])
    password2 = forms.CharField(required=True, validators=[validate_password])
class prescriptionform(forms.ModelForm):
    class Meta:
        model=prescription_book
        fields=["user","prescription_file","myself","others","others_choice","firstname","lastname","contact","age","gender"]
        # fields="__all__"
        # read_only_fields=["user"]
class selectedtestform(forms.ModelForm):
    class Meta:
        model=prescription_book
        # fields=["user","test_name",]
        fields="__all__"
        read_only_fields=["user"]
class subscriptionform(forms.ModelForm):
    class Meta:
        fields="__all__"
        model=subscription
        
class testnameform(forms.ModelForm):
    # here we only need to define the field we want to be editable
    test_name = forms.ModelMultipleChoiceField(
        queryset=test.objects.all(), required=False)
    
class testform(forms.ModelForm):
    price = forms.IntegerField(label="price")

    class Meta:
        model = test
        fields="__all__"