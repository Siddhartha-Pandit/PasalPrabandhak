
from django.urls import path
from .views import *

urlpatterns = [
    path('', indexview,name="account index"),
    path('CompanyRegister/', CompanyRegisterView.as_view(),name="account index"),
    path('login/', LoginView.as_view(),name="account index"),
    path('BranchRegister/', RegisterBranchView.as_view(),name="Branch index"),
    path('UserRegister/', UserRegisterView.as_view(),name="user index"),
    path('changepassword/', ChangePasswordView.as_view(),name="Change Password"),
    path('generateopt/', generateotpview.as_view(),name="generate opt"),
    path('verifyotp/', verityotp.as_view(),name="Verify otp"),
    path('forgotpassword/', forgotpasswordview.as_view(),name="forgot Password"),
    path('logout/', LogoutView.as_view(),name="logout view"),
    path('attandance/', AttendanceView.as_view(),name="attandance view"),
    path('allbranch/', BranchAllList.as_view(),name="branch view"),
    path('userAlllist/', UserAllListView.as_view(),name="branch view"),
    path('branchdetailview/', BranchDetailList.as_view(),name="branch view"),
    path('userdetailview/', UserAllDetailView.as_view(),name="branch view"),
]