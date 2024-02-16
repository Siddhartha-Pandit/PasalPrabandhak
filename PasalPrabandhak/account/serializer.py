from .models import User,Branch
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['email', 'fname', 'lname', 'branchid', 'iscmpid', 'companyid']


class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Branch
        fields='__all__'