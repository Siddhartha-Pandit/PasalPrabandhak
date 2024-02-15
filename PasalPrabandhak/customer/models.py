from django.db import models
from account.models import *
class Customer(models.Model):
    gender_choice=(
        ("M","Male"),
        ("F","Female"),
        ("O","Others")
    )
    phone=models.CharField(max_length=12,primary_key=True)
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    gender=models.CharField(max_length=20,choices=gender_choice)

    companyid=models.ForeignKey(Company,on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.phone

