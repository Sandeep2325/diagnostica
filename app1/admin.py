from tokenize import group
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
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
# Register your models here.
class cityadmin(admin.ModelAdmin):
    list_display=["cityname","created","updated"]
class testadmin(admin.ModelAdmin):
    list_display=["testt","categoryy","pricel1","pricel2","pricel3","pricel4","pricel5","pricel6","is_active","created","updated","action_btn"]
    list_editable=["is_active"]
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
                file_data = csv_file.read().decode("utf-8")
                csv_data = file_data.split("\r\n")
                print(csv_data[0])
                for x in csv_data[1:]:
                    fields = x.split(",")
                    try:
                        created = test.objects.create(
                            testt=fields[0],
                            categoryy=category.objects.get(pk=(fields[1])),
                            pricel1=fields[2],
                            pricel2=fields[3],
                            pricel3=fields[4],
                            pricel4=fields[5],
                            pricel5=fields[6],
                            pricel6=fields[7],
                            description=fields[8],)
                        created.save()
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
class prescriptionbookadmin(admin.ModelAdmin):
    list_display=["users","testname","myself","others","others_choice","firstname","lastname","contact","age","gender","prescription_file","created","updated","action_btn"]        
    readonly_fields=["user","myself","others","others_choice","firstname","lastname","contact","age","gender","unique"]
    exclude = ('unique',)
    # list_editable=[""]
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
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/prescription_book/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/prescription_book/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    def has_add_permission(self, request):
        return False
    # prepopulated_fields = {"slug": ("name",)}
# class selectedtestbookadmin(admin.ModelAdmin):
#     list_display=["id","user","testname","myself","others","others_choice","firstname","lastname","contact","age","gender","created","updated"]
#     def testname(self, obj):
#         return ", ".join([
#             test.testt for test in obj.test_name.all()
#         ])
#     testname.short_description = "Tests"
class categoryadmin(admin.ModelAdmin):
    list_display=["categoryy","created","updated","action_btn"]
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
    list_display=["package_title","testname","testcount","pricel1","pricel2","pricel3","pricel4","pricel5","pricel6","dpricel1","dpricel2","dpricel3","dpricel4","dpricel5","dpricel6","discount","created","updated","action_btn"]    
    readonly_fields=["created","updated"]
    # list_editable=["location"]
    prepopulated_fields = {"slug": ("package_title",)}
    summernote_fields = ('description')
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
    list_display=["package_name","testname","pricel1","pricel2","pricel3","pricel4","pricel5","pricel6","dpricel1","dpricel2","dpricel3","dpricel4","dpricel5","dpricel6","created","updated","action_btn"]
    readonly_fields=["created","updated"]
    # list_editable=["location"]
    prepopulated_fields = {"slug": ("package_name",)}
    # summernote_fields = ('content','package_name')
    def testname(self, obj):
        return ", ".join([
            test.testt for test in obj.test_name.all()
        ])
    testname.short_description = "Tests"
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/healthpackages/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/healthpackages/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
    
class healthsymptoms_admin(admin.ModelAdmin):
    list_display=["name","imagee","testname","symptoms","created","updated","action_btn"]
    prepopulated_fields = {"slug": ("name",)}
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
    list_display=["imagee","title","category","description","created","updated","action_btn"]
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
from django.utils.translation import gettext_lazy as _
class UserAdmin(OriginalUserAdmin): 
    list_display = ['username','email',"phone_no",'location','dob','gender','address','action_btn','date_joined']
    # list_editable=['is_confirmed']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name','last_name', 'email',"phone_no",'location','dob','gender','address')}),
    )
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
    list_display=["id","users","patient_infoo","booking_type","bookingdetails","amount","status","payment_status","created","updated","report","action_btn"]    
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
        try:
            html="<div><a  href='/admin/app1/prescription_book/"+ str(obj.testbooking_id)+"/change/'>{}</a></div>".format(str(obj.patient_info))
            return format_html(html)
        except:
            pass
    patient_infoo.short_description = "Patient Info"
    def has_add_permission(self, request):
        return False
class couponadmin(admin.ModelAdmin):
    list_display=["couponcode","discount","status"]
class cartadmin(admin.ModelAdmin):
    list_display=["user","items","categoryy","price","created","updated"]
class blogcategoryadmin(admin.ModelAdmin):
    list_display=["category","created","updated"]
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
class prescriptionbookadmin1(admin.ModelAdmin):

    def get_changelist(self, request, **kwargs):
        return testnamee

    def get_changelist_form(self, request, **kwargs):
        return testnameform
admin.site.register(city,cityadmin)
admin.site.register(blogcategory,blogcategoryadmin)
admin.site.register(test,testadmin)
admin.site.register(prescription_book,prescriptionbookadmin)
# admin.site.register(selectedtest_book,selectedtestbookadmin)
admin.site.register(User,UserAdmin)
admin.site.register(category,categoryadmin)
admin.site.register(healthcheckuppackages,healthcheckup_admin)
admin.site.register(healthpackages,healthpackage_admin)
admin.site.register(healthsymptoms,healthsymptoms_admin)
admin.site.register(healthcareblogs,healthcareblog_admin)
admin.site.register(testimonials,testimonialsadmin)
admin.site.register(book_history,bookhistoryadmin)
# admin.site.register(profile,profileadmin)
admin.site.register(aboutspan,aboutspanadmin)
admin.site.register(subscription,subscriptionadmin)
admin.site.register(socialmedialinks,socialmediaadmin)
admin.site.register(coupons,couponadmin)
# admin.site.register(pricee,priceadmin)
from django.contrib.auth.models import Group
admin.site.unregister(Group)
# admin.site.register(cart,cartadmin)




