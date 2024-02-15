from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Customer,Company
from . serializer import CustomerSerializers
from django.core.exceptions import ObjectDoesNotExist
def indexview(request):
    return HttpResponse("This is customer view")

class AddCustomerView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        phone= request.data.get('phone')
        fname= request.data.get('fname')
        lname= request.data.get('lname')
        gender= request.data.get('gender')
       

        if not phone or not fname or not lname or not gender:
            return Response({"error":"phone fname lanme gender address or pincode required"},status=status.HTTP_400_BAD_REQUEST)

        if Customer.objects.filter(phone=phone).exists():
            return Response({"error":"The user already exists"},status=status.HTTP_400_BAD_REQUEST)
        customer=Customer(phone=phone,fname=fname,lname=lname,gender=gender,companyid=user.companyid)
        customer.save()
        return Response({"message":"Customer is added"},status=status.HTTP_201_CREATED)

class GetCustomerView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        phone= request.data.get('phone')
        try:
            customer=Customer.objects.filter(phone=phone,companyid=user.companyid)
            if not customer:
                raise NotFound("Customer does not exist")
            print(customer)
            searilizer=CustomerSerializers(customer,many=True)
            
        except ObjectDoesNotExist:
            return Response({"error":"Customer does not exists"},status=status.HTTP_404_NOT_FOUND)

        return Response({"customer":searilizer.data},status=status.HTTP_302_FOUND)
    

class GetAllCustomerView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
       
        try:
            customer=Customer.objects.filter(companyid=user.companyid)
            if not customer:
                raise NotFound("Customer does not exist")
            print(customer)
            searilizer=CustomerSerializers(customer,many=True)
            return Response({"customer":searilizer.data},status=status.HTTP_302_FOUND)
            
        except ObjectDoesNotExist:
            return Response({"error":"Customer does not exists"},status=status.HTTP_404_NOT_FOUND)

    
        
        