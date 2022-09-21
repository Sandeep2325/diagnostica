from django.contrib import admin
from app1.models import *
from django.urls import path
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect,HttpResponse
from django.db import IntegrityError
from app1.forms import *
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.utils import get_attachment_model 
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
import csv
import re
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from app1.views import sms
# from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter
import datetime
from django.contrib.auth.models import Permission
# Register your models here.
class cityadmin(admin.ModelAdmin):
    list_display=["id","cityname","imagee","active","created","updated"]
    list_editable=["active"]
    def imagee(self, obj):
        # a=obj.image.first()
        # print(obj.image.first().image.url)
        try:
            # print(obj.image.url)
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.city_icon.url, "50", "50"))
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
    imagee.short_description = 'City Icon'
    # readonly_fields = ["cityname"]
class testadmin(admin.ModelAdmin):
    list_display=["testcode","testt","categoryy","Banglore_price","is_active","created","updated","action_btn"]
    list_editable=["is_active"]
    list_filter = ('categoryy', 'is_active')
    search_fields = ('testt', 'categoryy__categoryy')
    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("Mumbai_price","bhopal_price","nanded_price","pune_price","barshi_price","aurangabad_price")
        form = super(testadmin, self).get_form(request, obj, **kwargs)
        return form
    # form = testform
    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super(testadmin, self).get_fieldsets(request, obj)
    #     fieldsets[0][1]['fields'] += ['price']
    #     return fieldsets
    # prepopulated_fields = {"slug": ("testt",)}
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/test/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/test/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/test/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    def get_urls(self):
            urls = super().get_urls()
            new_urls = [path('upload-csv/', self.upload_csv), ]
            return new_urls + urls

    def upload_csv(self, request):
            if request.method == "POST":
                csv_file = request.FILES["csv_upload"]
                if not csv_file.name.endswith('.csv'):
                    messages.warning(
                        request, 'The wrong file type was uploaded')
                    return HttpResponseRedirect(request.path_info)
                def decode_utf8(input_iterator):
                    for l in input_iterator:
                        yield l.decode('cp1252')
                reader = csv.DictReader(decode_utf8(request.FILES['csv_upload']))
                for row in reader:
                    # print(row)
                    des = re.sub(r"</?\[\d+>", "", row.get("Description"))
                    try:
                        categoryy=category.objects.get(categoryy=row.get("category_id"))
                        testcode=row["Tests"]
                        b=testcode.split(" - ")
                        # print(b)
                        price=row.get("Banglore_price").strip().replace(",","")
                        price=int(price)
                        obj, created = test.objects.get_or_create(
                                testt=testcode,
                                testcode=b[0],
                                categoryy=categoryy,
                                Banglore_price=price if row.get("Banglore_price") else None,
                                Mumbai_price=row.get("Mumbai_price") if row.get("Mumbai_price") else None,
                                bhopal_price=row.get("bhopal_price") if row.get("bhopal_price") else None,
                                nanded_price=row.get("nanded_price") if row.get("nanded_price") else None,
                                pune_price=row.get("pune_price") if row.get("pune_price") else None,
                                barshi_price=row.get("barshi_price") if row.get("barshi_price") else None,
                                aurangabad_price=row.get("aurangabad_price") if row.get("aurangabad_price") else None,
                                description=des)
                    except IndexError:
                        pass
                    except (IntegrityError):
                        form = CsvImportForm()
                        data = {"form": form}
                        message = messages.warning(
                            request, 'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
                        return render(request, "admin/app1/csv_upload.html", data)
                url = reverse('admin:index')
                return HttpResponseRedirect(url)
            form = CsvImportForm()
            data = {"form": form}
            return render(request, "admin/app1/csv_upload.html", data)
from django.forms.widgets import SelectMultiple,MultiWidget
class prescriptionbookadmin(admin.ModelAdmin):
    list_display=["users","bookingid","testname","payment_status","paymentmethod","myself","others","others_choice","firstname","lastname","contact","age","gender","address","timeslot","prescription_file","report","created","updated","action_btn"]        
    readonly_fields=["user","myself","others","others_choice","firstname","lastname","contact","age","gender","created","updated","location","bookingid",'price']
    exclude = ('unique',)
    list_filter = ("myself","others",'paymentmethod','payment_status')
    search_fields = ('bookingid',)
    fieldsets = (
        (_('Prescription'), {'fields': ('user','prescription_file', 'test_name','price')}),
        (_('Coupon'),{'fields':('coupon',)}),
        (_('Patient Details'), {'fields': ("bookingid","payment_status","myself","others","others_choice","firstname","lastname","contact","age","gender","address","pincode","location","paymentmethod")}),
        (_('Report'),{'fields':("report",)}),
        (_('Comments'),{'fields':("comments",)})
    )
    autocomplete_fields = ['coupon']
    filter_horizontal = ('test_name',)
    # raw_id_fields = ("test_name",)
    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': SelectMultiple},
    # }
    # search_fields = ('testt', 'categoryy__categoryy')
    # list_editable=[""]
    
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("unique",)
        form = super(prescriptionbookadmin, self).get_form(request, obj, **kwargs)
        # print(obj.coupon)
        # a=form.base_fields["coupon"].queryset
        # a=coupons.objects.filter(couponcode=obj.coupon)
        # b=a.filter(couponcode=obj.coupon)
        # if b.exists():
        #     print("------------------")
        #     self.readonly_fields=["user","coupon","myself","others","others_choice","firstname","lastname","contact","age","gender","created","updated","location","bookingid",'price']
        # else:
        #     print("+++++++")
        #     self.readonly_fields=["user","myself","others","others_choice","firstname","lastname","contact","age","gender","created","updated","location","bookingid",'price']
        # print(b)
        # if b==
        # print("----------",a)
        # cleaned_data = super(form, self).clean()
        # cou=cleaned_data.get("coupon")
        # print(cou)
        # if form.base_fields["coupon"]!=None:
        #     self.readonly_fields=("coupon",)
        # self.fields['sku'].widget.attrs['readonly'] = True
        # form.base_fields['coupon'].widget.attrs['readonly'] = True
        return form
    def testname(self, obj):
        return ", ".join([
            test.testt for test in obj.test_name.all()
        ])
    testname.short_description = "Tests"
    def users(self,obj):
        try:
            html="<div><a  href='/admin/app1/user/"+ str(obj.user.id)+"/change/'>{}</a></div>".format(str(obj.user))
            return format_html(html)
        except:
            pass
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/prescriptionbook1/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/prescriptionbook1/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    
    def sendreportemail(self, request, queryset):
        for i in queryset:
            print("--------",bool(i.report))
            if (i.payment_status== True) and (bool(i.report) == True):
                send_mail(str("Tests Report | DIAGNOSTICA SPAN"),
                (f"Hi {i.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {i.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDIAGNOSTICA SPAN"),
                  settings.EMAIL_HOST_USER,
                  [i.user.email],
                  fail_silently=False)
                return messages.Success(request, 'Report Sent Successfully')
            elif(i.payment_status== False) and (bool(i.report) == True):
                return messages.warning(request, 'Payment Is Pending')
            elif(i.payment_status== True) and (bool(i.report) == False):
                return messages.warning(request, 'Please Upload Report')
            elif(i.payment_status== False) and (bool(i.report) == False):
                return messages.warning(request, 'Please Check Payment and Report')
    sendreportemail.short_description = "Report Email"
    
    def sendreportsms(self, request, queryset):
        for i in queryset:
            if (i.payment_status== True) and (bool(i.report) == True):
                message=f"Hi {i.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {i.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDIAGNOSTICA SPAN"
                sms(message,i.user.phone_no)
                return messages.Success(request, 'Report Sent Successfully')
            elif(i.payment_status== False) and (bool(i.report) == True):
                return messages.warning(request, 'Payment Is Pending')
            elif(i.payment_status== True) and (bool(i.report) == False):
                return messages.warning(request, 'Please Upload Report')
            elif(i.payment_status== False) and (bool(i.report) == False):
                return messages.warning(request, 'Please Check Payment and Report')
    sendreportsms.short_description = "Report SMS"
    actions = [sendreportsms,sendreportemail]
    # def reportt(self):
    #     print("hello")
    # def report_action(self, obj):
    #     html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/prescriptionbook1/" + \
    #         str(obj.id)+"/change/'></a><br></br>"
    #     html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/prescriptionbook1/"+str(obj.id)+"/delete/'></a></div>"
    #     return format_html(html)
    # report_action.short_description = "Report Action"
    def has_add_permission(self, request):
        return False

class testbookadmin(admin.ModelAdmin):
    list_display=["users","bookingid","tests","payment_status","myself","others","others_choice","firstname","lastname","contact","age","gender","address","pincode","date","timeslot","report","created","updated","action_btn"]        
    readonly_fields=["user","myself","payment_status","others","others_choice","firstname","lastname","contact","age","gender","created","updated","locationn",'bookingid']
    exclude = ('unique',)
    list_filter = ("myself","others","gender","payment_status")
    search_fields = ('bookingid',)
    # list_editable=[""]
    fieldsets = (
        (_('Tests'), {'fields': ('user','tests')}),
        (_('Patient Details'), {'fields': ("bookingid",'payment_status',"myself","others","others_choice","firstname","lastname","contact","age","gender","address","pincode","date","timeslot")}),
        (_('Report'),{'fields':("report",)}),
        (_('Comments'),{'fields':("comments",)})
    )
    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("unique",'price')
        form = super(testbookadmin, self).get_form(request, obj, **kwargs)
        return form
    def users(self,obj):
        try:
            html="<div><a  href='/admin/app1/user/"+ str(obj.user.id)+"/change/'>{}</a></div>".format(str(obj.user))
            return format_html(html)
        except:
            pass
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/testbook/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/testbook/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    def has_add_permission(self, request):
        return False
    def sendreportemail(self, request, queryset):
        # urll=request.build_absolute_uri('')
        for i in queryset:
            print("--------",bool(i.report.url))
            if (i.payment_status== True) and (bool(i.report) == True):
                send_mail(str("Tests Report | DIAGNOSTICA SPAN"),
                (f"Hi {i.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {i.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDIAGNOSTICA SPAN"),
                  settings.EMAIL_HOST_USER,
                  [i.user.email],
                  fail_silently=False)
                return messages.Success(request, 'Report Sent Successfully')
            elif(i.payment_status== False) and (bool(i.report) == True):
                return messages.warning(request, 'Payment Is Pending')
            elif(i.payment_status== True) and (bool(i.report) == False):
                return messages.warning(request, 'Please Upload Report')
            elif(i.payment_status== False) and (bool(i.report) == False):
                return messages.warning(request, 'Please Check Payment and Report')
    sendreportemail.short_description = "Report Email"
    def sendreportsms(self, request, queryset):
        for i in queryset:
            if (i.payment_status== True) and (bool(i.report) == True):
                message=f"Hi {i.user.first_name},\n Thank for using our Services.\nThis mail is regarding the booking id: {i.bookingid}\nYour report is successfully generated and has been uploaded in your dashboard. Please visit to review and download it..\nHope you liked our service. Have a healthy recovery.\nThank You,\nDIAGNOSTICA SPAN"
                sms(message,i.user.phone_no)
                return messages.Success(request, 'Report Sent Successfully')
            elif(i.payment_status== False) and (bool(i.report) == True):
                return messages.warning(request, 'Payment Is Pending')
            elif(i.payment_status== True) and (bool(i.report) == False):
                return messages.warning(request, 'Please Upload Report')
            elif(i.payment_status== False) and (bool(i.report) == False):
                return messages.warning(request, 'Please Check Payment and Report')
    sendreportsms.short_description = "Report SMS"
    actions = [sendreportsms,sendreportemail]
class categoryadmin(admin.ModelAdmin):
    list_display=["id","categoryy","created","updated","action_btn"]
    readonly_fields=["created","updated"]
    # prepopulated_fields = {"slug": ("categoryy",)}
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/category/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/test/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/category/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
class healthcheckup_admin(SummernoteModelAdmin):
    list_display=["package_title","dBanglore_price","created","updated","action_btn"]    
    readonly_fields=["created","updated"]
    filter_horizontal = ('test_name',)
    # list_editable=["location"]
    prepopulated_fields = {"slug": ("package_title",)}
    summernote_fields = ('description')
    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("discount","testcount","Banglore_price","test_name","Banglore_price","Mumbai_price","bhopal_price","nanded_price","pune_price","barshi_price","aurangabad_price","dMumbai_price","dbhopal_price","dnanded_price",'dpune_price','dbarshi_price','daurangabad_price',)
        form = super(healthcheckup_admin, self).get_form(request, obj, **kwargs)
        return form
    def testname(self, obj):
        return ", ".join([
            test.testt for test in obj.test_name.all()
        ])
    # def count(self,obj):
    #     a=obj.test_name.all().count()
    #     print(a)
    # testname.short_description = "Tests"
    
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/healthcheckuppackages/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/healthcheckuppackages/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
class healthpackage_admin(SummernoteModelAdmin):
    list_display=["package_name","Banglore_price","created","updated","action_btn"]
    readonly_fields=["created","updated"]
    # list_editable=["location"]
    prepopulated_fields = {"slug": ("package_name",)}
    # summernote_fields = ('content','package_name')
    filter_horizontal = ('test_name',)
    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("Mumbai_price","bhopal_price","nanded_price","pune_price","barshi_price","aurangabad_price","discounted_price",)
        form = super(healthpackage_admin, self).get_form(request, obj, **kwargs)
        return form
    # def testname(self, obj):
    #     return ", ".join([
    #         test.testt for test in obj.test_name.all()
    #     ])
    # testname.short_description = "Tests"
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/healthpackages/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/healthpackages/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    def get_urls(self):
            urls = super().get_urls()
            new_urls = [path('upload-csv/', self.upload_csv), ]
            return new_urls + urls

    def upload_csv(self, request):
            if request.method == "POST":
                csv_file = request.FILES["csv_upload"]
                if not csv_file.name.endswith('.csv'):
                    messages.warning(
                        request, 'The wrong file type was uploaded')
                    return HttpResponseRedirect(request.path_info)
                def decode_utf8(input_iterator):
                    for l in input_iterator:
                        yield l.decode('cp1252')
                reader = csv.DictReader(decode_utf8(request.FILES['csv_upload']))
                for row in reader:
                    des = re.sub(r"</?\[\d+>", "", row.get("Description"))
                    print(row)
                    try:
                        tests=test.objects.get_or_create(testt=row.get("Test Name"))
                        if row.get("basic")=="Y":
                            a=healthpackages.objects.get(package_name="Basic")
                            a.test_name.add(tests)
                        if row.get("standard")=="Y":
                             a=healthpackages.objects.get(package_name="Standard")
                             a.test_name.add(tests)
                        if row.get("starter")=="Y":
                             a=healthpackages.objects.get(package_name="Starter")
                             a.test_name.add(tests)
                        # obj, created = healthpackages.objects.get_or_create(
                        #         testt=row["Tests"],
                        #         testcode=row["test_code"],
                        #         categoryy=categoryy,
                        #         Banglore_price=row.get("Banglore_price") if row.get("Banglore_price") else None,
                        #         Mumbai_price=row.get("Mumbai_price") if row.get("Mumbai_price") else None,
                        #         bhopal_price=row.get("bhopal_price") if row.get("bhopal_price") else None,
                        #         nanded_price=row.get("nanded_price") if row.get("nanded_price") else None,
                        #         pune_price=row.get("pune_price") if row.get("pune_price") else None,
                        #         barshi_price=row.get("barshi_price") if row.get("barshi_price") else None,
                        #         aurangabad_price=row.get("aurangabad_price") if row.get("aurangabad_price") else None,
                        #         description=des)
                    except IndexError:
                        pass
                    except (IntegrityError):
                        form = CsvImportForm()
                        data = {"form": form}
                        message = messages.warning(
                            request, 'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
                        return render(request, "admin/app1/csv_upload.html", data)
                url = reverse('admin:index')
                return HttpResponseRedirect(url)
            form = CsvImportForm()
            data = {"form": form}
            return render(request, "admin/app1/csv_upload.html", data)
    
class healthsymptoms_admin(SummernoteModelAdmin):
    list_display=["name","testname","discounted_price","created","updated","action_btn"]
    readonly_fields=["created","updated"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('test_name',)
    summernote_fields = ('symptoms',)
    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ("Banglore_price","Mumbai_price","bhopal_price","nanded_price","pune_price","barshi_price","aurangabad_price",)
        form = super(healthsymptoms_admin, self).get_form(request, obj, **kwargs)
        return form
    def testname(self, obj):
        return ", ".join([
            test.testt for test in obj.test_name.all()
        ])
    testname.short_description = "Tests"
    def imagee(self, obj):
        # a=obj.image.first()
        # print(obj.image.first().image.url)
        try:
            # print(obj.image.url)
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.image.url, "50", "50"))
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
    imagee.short_description="Image"
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/healthsymptoms/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/healthsymptoms/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
class healthcareblog_admin(SummernoteModelAdmin):
    list_display=["imagee","title","category","created","updated","action_btn"]
    readonly_fields=["created","updated"]
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ('description',)
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/healthcareblogs/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/healthcareblogs/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    def imagee(self, obj):
        # a=obj.image.first()
        # print(obj.image.first().image.url)
        try:
            # print(obj.image.url)
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.image.url, "50", "50"))
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
    imagee.short_description = 'Image'
class testimonialsadmin(admin.ModelAdmin):
    list_display=["username","imagee","description","created","updated",]
    readonly_fields=["created","updated"]
    def imagee(self, obj):
        # a=obj.image.first()
        # print(obj.image.first().image.url)
        try:
            # print(obj.image.url)
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.photo.url, "50", "50"))
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
class profileadmin(admin.ModelAdmin):
    list_display=["user","imagee","name","email","phone_no","gender","location","dob","created","updated",]
    readonly_fields=["created","updated"]
    prepopulated_fields = {"slug": ("name",)}
    def imagee(self, obj):
        # a=obj.image.first()
        # print(obj.image.first().image.url)
        try:
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.photo.url, "50", "50"))
            
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
    imagee.short_description = 'Image'
class aboutspanadmin(admin.ModelAdmin):
    list_display=["description1","testedpeople","verifiedcenter","cities","dailyvisits","created","updated","action_btn"]
    readonly_fields=["created","updated"]
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/aboutspan/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/aboutspan/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
class socialmediaadmin(admin.ModelAdmin):
    list_display=["name","url"]
    # def has_add_permission(self, request):
    #     if self.model.objects.count() >= 1:
    #         return False
    #     return super().has_add_permission(request)

class UserAdmin(OriginalUserAdmin): 
    list_display = ['id','first_name','last_name','email',"phone_no",'age','gender','location','address','date_joined','action_btn']
    # list_editable=['is_confirmed']
    fieldsets = (
        (None, {'fields': ('email', 'password','aggregator')}),
        (_('Personal info'), {'fields': ('photo','first_name','last_name', "phone_no",'age','gender','location','address',)}),
        (
            _("Permissions"),
            {
                "fields": (
                    # "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    # def has_delete_permission(self, request,obj=None):
    #     return False
    def get_form(self, request, obj=None, **kwargs):
        # Get form from original UserAdmin.
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        if 'user_permissions' in form.base_fields:
            permissions = form.base_fields['user_permissions']
            permissions.queryset = permissions.queryset.exclude(content_type__app_label__in=['admin', 'auth','sessions','django_summernote','contenttypes','admin_black','django_celery','django_celery_beat'])
        return form
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/user/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/user/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/user/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
class subscriptionadmin(admin.ModelAdmin):
    list_display=["email","created"]
class bookhistoryadmin(admin.ModelAdmin):
    list_display=["bookingid","users","patient_infoo","booking_type","bookingdetails","amount","status","payment_status","created","updated","action_btn"]    
    readonly_fields=["created","updated",'bookingid','payment_id']
    list_filter = ("payment_status","booking_type")
    search_fields = ('bookingid','payment_id')
    def get_form(self, request, obj=None, **kwargs):
        # if obj.type == "1":
        self.exclude = ('testbooking_id','report','uni' )
        form = super(bookhistoryadmin, self).get_form(request, obj, **kwargs)
        return form
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/book_history/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/book_history/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    def users(self,obj):
        try:
            html="<div><a  href='/admin/app1/user/"+ str(obj.user.id)+"/change/'>{}</a></div>".format(str(obj.user))
            return format_html(html)
        except:
            pass
    def patient_infoo(self,obj):
        # admin/app1/prescription_book/56/change/
        if obj.booking_type=="Prescription":
            try:
                a=Prescriptionbook1.objects.get(bookingid=obj.bookingid)
                html="<div><a  href='/admin/app1/prescriptionbook1/"+ str(a.id)+"/change/'>{}</a></div>".format(str(obj.patient_info))
                return format_html(html)
            except:
                pass
        else:
            try:
                a=testbook.objects.get(bookingid=obj.bookingid)
                html="<div><a  href='/admin/app1/testbook/"+ str(a.id)+"/change/'>{}</a></div>".format(str(obj.patient_info))
                return format_html(html)
            except:
                pass
    patient_infoo.short_description = "Patient Info"
    def has_add_permission(self, request):
        return False
class couponadmin(admin.ModelAdmin):
    list_display=["couponcode","discount","Locations","limit","status","startdate","enddate","created","updated","action_btn"]
    list_filter=["cityy","status"]
    # list_filter=(
    #     ("cityy",RelatedDropdownFilter),
    #     ("couponcode",DropdownFilter),)
    search_fields=["couponcode"]
    list_editable=["status"]
    filter_horizontal = ('cityy',)
    def Locations(self, obj):
        return ", ".join([
            city.cityname for city in obj.cityy.all()
        ])
    Locations.short_description = "Locations"
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/coupons/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/coupons/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),path('export-csv/', self.export)]
        return new_urls + urls
    def upload_csv(self, request):
            if request.method == "POST":
                csv_file = request.FILES["csv_upload"]
                if not csv_file.name.endswith('.csv'):
                    messages.warning(
                        request, 'The wrong file type was uploaded')
                    return HttpResponseRedirect(request.path_info)
                def decode_utf8(input_iterator):
                    for l in input_iterator:
                        yield l.decode('cp1252')
                reader = csv.DictReader(decode_utf8(request.FILES['csv_upload']))
                for row in reader:
                    try:
                        try:
                            coupons.objects.get(couponcode=row["ï»¿Coupon_Code"])
                            form = CsvImportForm()
                            data = {"form": form}
                            messages.warning(request,row["ï»¿Coupon_Code"]+" Already Exists")
                            return render(request, "admin/app1/csv_upload.html", data)
                        except:
                            startdate = datetime.datetime.strptime(row["startdate"], '%d-%m-%Y %H:%M')
                            enddate = datetime.datetime.strptime(row["enddate"], '%d-%m-%Y %H:%M')
                            cityname=row.get("city_id")
                            citynamee=cityname.split(",")
                            # cityy=city.objects.get(pk=row.get("city_id"))
                            obj, created = coupons.objects.get_or_create(
                                    couponcode=row["ï»¿Coupon_Code"],
                                    discount=row["Discount"],
                                    limit=row["limit"],
                                    status=row["status"],
                                    startdate=startdate,
                                    enddate=enddate,
                                    )
                            for citi in citynamee:
                                cityy=city.objects.get(id=citi)
                                obj.cityy.add(cityy)
                    # except IndexError:
                    #     pass
                    except (IntegrityError):
                        form = CsvImportForm()
                        data = {"form": form}
                        message = messages.warning(
                            request, 'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
                        return render(request, "admin/app1/csv_upload.html", data)
                    except Exception as e:
                        form = CsvImportForm()
                        data = {"form": form}
                        message = messages.warning(
                            request, e)
                        return render(request, "admin/app1/csv_upload.html", data)
                url = reverse('admin:index')
                return HttpResponseRedirect(url)
            form = CsvImportForm()
            data = {"form": form}
            return render(request, "admin/app1/csv_upload.html", data) 
    def export(self,request):
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="couponsdata.csv"'},)
        # response = HttpResponse(
        # content_type='application/ms-excel',
        # headers={'Content-Disposition': 'attachment; filename="couponsdata.xls"'},)
        writer = csv.writer(response)
        writer.writerow(["Coupon Code","Discount","limit","Locations","status","start Date","End Date","Created","Updated"])
        for i in coupons.objects.all():
            def Locations():
                return ", ".join([
                city.cityname for city in i.cityy.all()
                ])
            writer.writerow([i.couponcode,i.discount,i.limit,Locations(),i.status,i.startdate,i.enddate,i.created,i.updated])
        return response
    # readonly_fields=["created","updated"]
class cartadmin(admin.ModelAdmin):
    list_display=["user","items","categoryy","price","created","updated"]
class blogcategoryadmin(admin.ModelAdmin):
    list_display=["category","created","updated"]
    readonly_fields=["created","updated"]
    prepopulated_fields = {"slug": ("category",)}
class testnamee(ChangeList):
    def __init__(self, request, model, list_display,
        list_display_links, list_filter, date_hierarchy,
        search_fields, list_select_related, list_per_page,
        list_max_show_all, list_editable, model_admin):
        
        super(testnamee, self).__init__(request, model,
            list_display, list_display_links, list_filter,
            date_hierarchy, search_fields, list_select_related,
            list_per_page, list_max_show_all, list_editable, 
            model_admin)
        # these need to be defined here, and not in MovieAdmin
        self.list_display = "id","user","test_name","myself","others","others_choice","firstname","lastname","contact","age","gender","prescription_file","created","updated"
    # self.list_display_links = ['name']
        self.list_editable = ['test_name']
class priceadmin(admin.ModelAdmin):
    list_display=["testt","city","price"]
class paymentadmin(admin.ModelAdmin):
    list_display=["user","paymentid","transid","amount","date"]
    search_fields=["user__first_name","paymentid","transid"]
    def has_add_permission(self, request):
        return False
class contactusadmin(admin.ModelAdmin):
    list_display=["fullname","email","phone","subject","message",'created','updated']
    search_fields=["fullname","email","phone"]
class faqadmin(admin.ModelAdmin):
    list_display=["question","answer"]
    search_fields=["question","answer"]
class invoiceadmin(admin.ModelAdmin):
    list_display=['order_id',"items","labtest","packages","healthsymptoms","price"]
    search_fields=["order_id","items"]
class couponredeemadmin(admin.ModelAdmin):
    list_display=["user","booking_id",'order_id',"coupon","discountpercen","discountamount","created",]
    search_fields=["user__first_name","booking_id","coupon","order_id","user"]
    def export(self,request,queryset):
        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="redeemedcoupon.csv"'},)
        writer = csv.writer(response)
        writer.writerow(["User","Order_id","Coupon","Discount Percent","Discount Amount","Actual Amount","Created"])
        for i in queryset:
            writer.writerow([i.user,i.order_id,i.coupon,i.discountpercen,i.discountamount,i.actualamount,i.created])
        return response
    actions = [export]
class requestadmin(admin.ModelAdmin):
    list_display=['firstname','lastname','phone','email','message','created','updated']
class invoiceeadmin(admin.ModelAdmin):
    list_display=['user','order_id','file','created','updated']
    
    def has_add_permission(self, request):
        return False
    
    
    # def has_delete_permission(self, request,obj=None):
    #     return False
admin.site.register(User,UserAdmin)
admin.site.register(faq,faqadmin)
admin.site.register(contactus,contactusadmin)
admin.site.register(payment,paymentadmin)
admin.site.register(city,cityadmin)
admin.site.register(blogcategory,blogcategoryadmin)
admin.site.register(test,testadmin)
# admin.site.register(prescription_book,prescriptionbookadmin)
admin.site.register(testbook,testbookadmin)
admin.site.register(Prescriptionbook1,prescriptionbookadmin)
admin.site.register(category,categoryadmin)
admin.site.register(healthcheckuppackages,healthcheckup_admin)
admin.site.register(healthpackages,healthpackage_admin)
admin.site.register(healthsymptoms,healthsymptoms_admin)
admin.site.register(healthcareblogs,healthcareblog_admin)
admin.site.register(testimonials,testimonialsadmin)
admin.site.register(book_history,bookhistoryadmin)
# admin.site.register(profile,profileadmin)
# admin.site.register(aboutspan,aboutspanadmin)
admin.site.register(subscription,subscriptionadmin)
# admin.site.register(socialmedialinks,socialmediaadmin)
admin.site.register(coupons,couponadmin)
admin.site.register(couponredeem,couponredeemadmin)
# admin.site.register(invoicee,invoiceadmin)
admin.site.register(requestcall,requestadmin)
admin.site.unregister(get_attachment_model())
admin.site.register(invoicee,invoiceeadmin)
class MyGroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')

    permissions = forms.ModelMultipleChoiceField(
        Permission.objects.exclude(content_type__app_label__in=['admin', 'auth','sessions','django_summernote','contenttypes','admin_black','django_celery','django_celery_beat']),
        widget=admin.widgets.FilteredSelectMultiple(_('permissions'), False))

class MyGroupAdmin(admin.ModelAdmin):
    form = MyGroupAdminForm
    search_fields = ('name',)
    ordering = ('name',)

admin.site.unregister(Group)
admin.site.register(Group, MyGroupAdmin)
# admin.site.register(Permission)




