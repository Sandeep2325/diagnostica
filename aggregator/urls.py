from django.urls import path
from aggregator import views

urlpatterns = [
    path('',views.loginn,name="aggregator-login"),
    path('dashboard',views.dashboardd.as_view(),name="aggregator-dashboardd"),
    path("logout",views.aggregatorlogout_request, name="aggregator-logout"),
]
