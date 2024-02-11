
from django.urls import path
from .views import *

urlpatterns = [
    path('', indexview,name="account index"),
    path('CompanyRegister/', CompanyRegisterView.as_view(),name="account index"),
    path('login/', LoginView.as_view(),name="account index"),
    path('BranchRegister/', RegisterBranchView.as_view(),name="Branch index"),
]