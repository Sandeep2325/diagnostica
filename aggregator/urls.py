from django.urls import path
from aggregator import views
# from diagnostica.aggregator.views import detailtest

urlpatterns = [
    path('login',views.loginn,name="aggregator-login"),
    path('dashboard',views.dashboardd.as_view(),name="aggregator-dashboardd"),
    path("logout",views.aggregatorlogout_request, name="aggregator-logout"),
    path("dashboard/add",views.addform.as_view(), name="addform"),
    path("aggregatortest",views.aggregatortests,name="aggregatortest"),
    path("",views.aggregatorprofile.as_view(),name="aggregator-profile"),
    path("change-password",views.changepassword.as_view(),name="aggregator-changepassword"),
    path("<bookingid>/test-details",views.detailtest.as_view(),name="test-detailss"),
]
