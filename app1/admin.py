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
# Register your models here.
class testadmin(admin.ModelAdmin):
    list_display=["id","testt","description","categoryy","price","created","updated","action_btn"]
    prepopulated_fields = {"slug": ("testt",)}
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
                for x in csv_data:
                    fields = x.split(",")
                    try:
                        created = test.objects.create(
                            testt=fields[0],
                            categoryy=category.objects.get(pk=(fields[1])),
                            price=fields[2],
                            description=fields[3],)
                        created.save()
                    except IndexError:
                        pass
                    except (IntegrityError):
                        form = CsvImportForm()
                        data = {"form": form}
                        message = messages.warning(
                            request, 'Something went wrong! check your file again \n 1.Upload correct file \n 2.Check you data once')
                        return render(request, "admin/csv_upload.html", data)
                url = reverse('admin:index')
                return HttpResponseRedirect(url)
            form = CsvImportForm()
            data = {"form": form}
            return render(request, "admin/csv_upload.html", data)
class prescriptionbookadmin(admin.ModelAdmin):
    list_display=["id","user","testname","myself","others","others_choice","firstname","lastname","contact","age","gender","prescription_file","created","updated"]        
    def testname(self, obj):
        return ", ".join([
            test.testt for test in obj.test_name.all()
        ])
    testname.short_description = "Tests"
    # prepopulated_fields = {"slug": ("name",)}
# class selectedtestbookadmin(admin.ModelAdmin):
#     list_display=["id","user","testname","myself","others","others_choice","firstname","lastname","contact","age","gender","created","updated"]
#     def testname(self, obj):
#         return ", ".join([
#             test.testt for test in obj.test_name.all()
#         ])
#     testname.short_description = "Tests"
class categoryadmin(admin.ModelAdmin):
    list_display=["id","categoryy","created","updated","action_btn"]
    prepopulated_fields = {"slug": ("categoryy",)}
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/category/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/test/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/category/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
class healthcheckup_admin(SummernoteModelAdmin):
    list_display=["id","package_title","testname","test_nos","description","actual_price","discounted_price","discount","created","updated","action_btn"]    
    readonly_fields=["discounted_price","test_nos"]
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
    list_display=['id',"package_name","testname","actual_price","discounted_price","discount","created","updated","action_btn"]
    readonly_fields=["discounted_price",]
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
    list_display=["id","name","testname","symptoms","created","updated","action_btn"]
    prepopulated_fields = {"slug": ("name",)}
    def testname(self, obj):
        return ", ".join([
            test.testt for test in obj.test_name.all()
        ])
    testname.short_description = "Tests"
    
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/healthsymptoms/" + \
            str(obj.id)+"/change/'></a><br></br>"
        # html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/healthpackages/" + \
        #     str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/healthsymptoms/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
class healthcareblog_admin(admin.ModelAdmin):
    list_display=["id","imagee","title","description","created","updated","action_btn"]
    prepopulated_fields = {"slug": ("title",)}
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
            print(obj.image.url)
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.image.url, "50", "50"))
            
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
    imagee.short_description = 'Image'
class testimonialsadmin(admin.ModelAdmin):
    list_display=["id","username","imagee","description","created","updated",]
    def imagee(self, obj):
        # a=obj.image.first()
        # print(obj.image.first().image.url)
        try:
            # print(obj.image.url)
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.photo.url, "50", "50"))
            
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
class profileadmin(admin.ModelAdmin):
    list_display=["id","user","imagee","name","email","phone_no","gender","location","dob","created","updated",]
    prepopulated_fields = {"slug": ("name",)}
    def imagee(self, obj):
        # a=obj.image.first()
        # print(obj.image.first().image.url)
        try:
            print(obj.image.url)
            return format_html('<img src="{}" width="{}" height="{}"/>'.format(obj.photo.url, "50", "50"))
            
        except:
            return format_html('<img src="https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg" width="100" height="100"/>')
    imagee.short_description = 'Image'
class aboutspanadmin(admin.ModelAdmin):
    list_display=["id","description1","testedpeople","verifiedcenter","cities","dailyvisits","created","updated","action_btn"]
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
    list_display=["id","name","url"]
    # def has_add_permission(self, request):
    #     if self.model.objects.count() >= 1:
    #         return False
    #     return super().has_add_permission(request)
class UserAdmin(OriginalUserAdmin): 
    list_display = ['id','username', 'email','is_staff', 'phone_no','action_btn','date_joined']
    # list_editable=['is_confirmed']
    def action_btn(self, obj):
        html = "<div class='field-action_btn d-flex m-8'> <a class='fa fa-edit ml-2' href='/admin/app1/user/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-success fa fa-eye ml-2' href='/admin/app1/user/" + \
            str(obj.id)+"/change/'></a><br></br>"
        html += "<a class='text-danger fa fa-trash ml-2' href='/admin/app1/user/"+str(obj.id)+"/delete/'></a></div>"
        return format_html(html)
    action_btn.short_description = "Action"
class subscriptionadmin(admin.ModelAdmin):
    list_display=["id","email","created"]
class bookhistoryadmin(admin.ModelAdmin):
    list_display=["id","user","patient_info","booking_type","bookingdetails","amount","status","payment_status","created","updated","report"]    
class couponadmin(admin.ModelAdmin):
    list_display=["id","couponcode","discount","startdate","enddate"]
class cartadmin(admin.ModelAdmin):
    list_display=["id","user","items","categoryy","price","created","updated"]
# admin.site.register(User, UserAdmin)

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
admin.site.register(profile,profileadmin)
admin.site.register(aboutspan,aboutspanadmin)
admin.site.register(subscription,subscriptionadmin)
admin.site.register(socialmedialinks,socialmediaadmin)
admin.site.register(coupons,couponadmin)
admin.site.register(cart,cartadmin)
