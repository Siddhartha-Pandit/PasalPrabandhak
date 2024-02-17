from .models import User,Branch
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'fname', 'lname', 'branchid', 'iscmpid', 'companyid', 
                  'is_staff', 'is_active', 'is_billing_clerk', 'isaddstock', 
                  'isaddbranch', 'iseditbranch', 'isviewbranch', 'isdeletebranch', 
                  'isadduser', 'isdeleteuser', 'isedituser', 'isviewuser', 
                  'iseditstock', 'iseviewstock', 'isedeletestock', 'isaddcustomer', 
                  'isdeletecompany', 'istakeattendance']


class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields='__all__'