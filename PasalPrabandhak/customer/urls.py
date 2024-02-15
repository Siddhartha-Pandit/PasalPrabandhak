
from django.urls import path
from .views import *

urlpatterns = [
    path('', indexview,name="account index"),
    path('addcustomer/',AddCustomerView.as_view() ,name="add customer"),
    path('getcustomer/',GetCustomerView.as_view() ,name="add customer"),
    path('getallcustomer/',GetAllCustomerView.as_view() ,name="add customer"),
   
]