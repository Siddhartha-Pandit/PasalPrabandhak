from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Company,User
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
def indexview(request):
    return HttpResponse("This is account view")

class CompanyRegisterView(APIView):
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        companyname=request.data.get('companyname')
        address=request.data.get('address')
        pincode=request.data.get('pincode')
        lat=request.data.get('lat')
        long=request.data.get('long')
        print(f"{email} {password} {companyname} {address}, {pincode},{lat},{long}")
        if not email or not password or not companyname or not address or not pincode or not lat or not long:
            return Response({"error":"email, name,address,pincod, latitude and longitude is required"},status=status.HTTP_400_BAD_REQUEST)
        
        if Company.objects.filter(email=email).exists():
            return Response({"Error":"The company with this id already exists"},status=status.HTTP_400_BAD_REQUEST)
    
        company=Company(email=email,companyname=companyname,address=address,pincode=pincode,lat=lat,long=long)
        company.save()
        user=User.objects.create_user(email=email,password=password,iscmpid=True,companyid=company)
        return Response({"message":"The company registedred sucessfully"},status=status.HTTP_201_CREATED)

  
class LoginView(APIView):
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')

        if not email or not password:
            return Response({"error":"Email and password is required"},status=status.HTTP_400_BAD_REQUEST)
        
        user=authenticate(email=email,password=password)

        if user is not None:
            login(request,user)
            refresh=RefreshToken.for_user(user)
            return Response({'refresh':str(refresh),"access":str(refresh.access_token)},status=status.HTTP_200_OK)
        
        else:
            return Response({"error":"Login faild invalid email or password"})