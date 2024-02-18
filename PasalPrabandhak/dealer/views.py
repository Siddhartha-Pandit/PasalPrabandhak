from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from . models import Dealer,Category,Stock

def indexview(request):
    return HttpResponse("This is dealer")

class AddDealerView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        legalidno=request.data.get('legalidno')
        companyname=request.data.get('companyname')
        phone=request.data.get('phone')
        address=request.data.get('address')
        
        contactperson_fname=request.data.get('contactperson_fname')
        contactperson_lname=request.data.get('contactperson_lname')
        contactperson_contact=request.data.get('contactperson_contact')
        contactperson_email=request.data.get('contactperson_email')
   
    
    # companyid=models.ForeignKey(Company,on_delete=models.CASCADE)
        
        dealer=Dealer(legalidno=legalidno,companyname=companyname,phone=phone,address=address,contactperson_fname=contactperson_fname,contactperson_lname=contactperson_lname,contactperson_contact=contactperson_contact,contactperson_email=contactperson_email,companyid=user.companyid)
        dealer.save()
        