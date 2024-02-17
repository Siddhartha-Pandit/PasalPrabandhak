from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import usermanager
from django.utils import timezone
from datetime import datetime
import random
class Company(models.Model):
    email=models.CharField(max_length=255,primary_key=True,null=False,default='')
    companyname=models.CharField(max_length=255,null=False,default='')
    address=models.CharField(max_length=255,null=False)
    pincode=models.CharField(max_length=20,null=False)
    lat=models.CharField(max_length=100)
    long=models.CharField(max_length=100)

    def __str__(self):
        return self.email
    

class Branch(models.Model):
    branch_id=models.CharField(max_length=255,primary_key=True,null=False)
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    address=models.CharField(max_length=255,null=False)
    pincode=models.CharField(max_length=20,null=False)
    lat=models.CharField(max_length=100)
    long=models.CharField(max_length=100)
    def __str__(self):
        return self.branch_id

class User(AbstractBaseUser,PermissionsMixin):
    email=models.CharField(max_length=255,primary_key=True,null=False)
    fname=models.CharField(max_length=255,null=True)
    lname=models.CharField(max_length=255,null=True)
    branchid=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    iscmpid=models.BooleanField(default=False)
    isbraid=models.BooleanField(default=False)
    isadduser=models.BooleanField(default=False)
    companyid=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_billing_clerk=models.BooleanField(default=False)
    isaddstock=models.BooleanField(default=False)
    isaddbranch=models.BooleanField(default=False)
    iseditbranch=models.BooleanField(default=False)
    isviewbranch=models.BooleanField(default=False)
    isdeletebranch=models.BooleanField(default=False)
    isadduser=models.BooleanField(default=False)
    isdeleteuser=models.BooleanField(default=False)
    isedituser=models.BooleanField(default=False)
    isviewuser=models.BooleanField(default=False)
    isaddstock=models.BooleanField(default=False)
    iseditstock=models.BooleanField(default=False)
    iseviewstock=models.BooleanField(default=False)
    isedeletestock=models.BooleanField(default=False)
    isaddcustomer=models.BooleanField(default=False)
    isdeletecompany=models.BooleanField(default=False)
    istakeattendance=models.BooleanField(default=False)
    
    
    username=None
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=usermanager()

    def __str__(self):
        return self.email
    
class Subscription(models.Model):
    subscription_id=models.AutoField(primary_key=True,null=False)
    subscription_name=models.CharField(max_length=255)
    description=models.CharField(max_length=2000)
    price=models.IntegerField()


    def __str__(self):
        subscription_id=str(self.subscription_id)
        return subscription_id
    
class Subscription_purchase(models.Model):
    purchase_id=models.AutoField(primary_key=True,null=False)
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    subscription_id=models.ForeignKey(Subscription,on_delete=models.SET_NULL,null=True)
    purchase_date=models.DateTimeField(null=False)
    expiry_date=models.DateTimeField(null=False)

    def __str__(self):
        purchase_id=str(self.purchase_id)
        return self.purchase_id


class attandance(models.Model):
    attandance_id=models.AutoField(primary_key=True,null=False)
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    time=models.DateTimeField(null=False)
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    branch_id=models.ForeignKey(Branch,on_delete=models.CASCADE)
    ipaddress = models.CharField(max_length=45, null=True, blank=True)
    def __str__(self):
        attandance_id=str(self.attandance_id)
        return attandance_id


class OTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.IntegerField()
    generatedtime=models.DateTimeField()
    used=models.BooleanField()
    
    def is_expired(self):
        expiration_time=timezone.now()-timezone.timedelta(minutes=5)
        return self.generatedtime<expiration_time

    @classmethod
    def generate_otp(cls,email):
        try:
            user = User.objects.get(email=email)
            otp_value = random.randint(100000, 999999)
            otp_instance = cls.objects.create(user=user, otp=otp_value, generatedtime=timezone.now(), used=False)
            return otp_instance
        except User.DoesNotExist:
            return None
        

