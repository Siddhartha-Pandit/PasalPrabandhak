from django.db import models
from account.models import *

class Dealer(models.Model):
    legalidno=models.CharField(primary_key=True,max_length=255,null=False,default='')
    companyname=models.CharField(max_length=255)
    phone=models.CharField(max_length=12)
    address=models.CharField(max_length=255)
    contactperson_fname=models.CharField(max_length=255)
    contactperson_lname=models.CharField(max_length=255)
    contactperson_contact=models.CharField(max_length=255)
    contactperson_email=models.CharField(max_length=255)
    companyid=models.ForeignKey(Company,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.dealerid)
    

class Category(models.Model):
    unitchoice=(
        ('Pcs',"Pieces"),
        ('doz',"Dozones"),
        ('ctn',"Carton"),
        ('kg',"Kilogram"),
        ('g',"gram"),
        ('MT',"Metric Ton"),
        ('oz',"Ounce"),
        ('t',"Ton"),
        ('lb',"Pound"),
        ('l',"Liter"),
        ('ml',"Milliliter"),
        ('m',"Meter"),
        ('sqm',"Square Meter"),
        ('cbm',"Cubic Meter"),
    )
    categoryid=models.AutoField(primary_key=True)
    categoryname=models.CharField(max_length=255)
    categoryunit=models.CharField(max_length=50,choices=unitchoice)

    def __str__(self):
        return str(self.categoryid)


class Stock(models.Model):
    barcode=models.CharField(max_length=255,primary_key=True)
    name=models.CharField(max_length=255)
    mfgdate=models.DateField()
    expirydate=models.DateField()
    costprice=models.FloatField()
    sellingprice=models.FloatField()
    mrp=models.FloatField()
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='category_stock')
    unit=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='unit_stock')
    dealer=models.ForeignKey(Dealer,on_delete=models.SET_NULL,null=True)

    def __Str__(self):
        return self.barcode