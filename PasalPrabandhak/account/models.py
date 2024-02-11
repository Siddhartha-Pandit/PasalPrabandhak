from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import usermanager

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
    companyid=models.ForeignKey(Company,on_delete=models.CASCADE,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
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

    def __str__(self):
        attandance_id=str(self.attandance_id)
        return attandance_id

