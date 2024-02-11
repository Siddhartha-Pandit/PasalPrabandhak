from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Company,User,Branch
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from . serializer import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
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
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error":"Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            companydata=None
            try:
                company=Company.objects.get(email=email)
                companydata={
                    "companyname":company.companyname,
                    "address":company.address,
                    "pincode":company.pincode
                }
            except ObjectDoesNotExist:
                pass
            serializer = UserSerializer(user) 
            # return Response({'refresh': str(refresh), 'access': str(refresh.access_token), 'data': serializer.data,'companydata':companydata}, status=status.HTTP_200_OK)
            return Response({'refresh':str(refresh),'access':str(refresh.access_token)}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error":"Login failed invalid email or password"})

class RegisterBranchView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        cmpemail=request.data.get('cmpemail')
        branch_id=request.data.get('branch_id')
        branchpassword=request.data.get('branchpassword')
        branchaddress=request.data.get('branchaddress')
        branchpincode=request.data.get('pincode')
        branchlat=request.data.get('lat')
        branchlong=request.data.get('long')

        if not cmpemail  or not branchpassword or not branchaddress or not branchpincode or not branchlat or not branchlong:
            return Response({"error":"All the data is not provided please provide all data"},status=status.HTTP_400_BAD_REQUEST)
        
        if Branch.objects.filter(branch_id=branch_id).exists():
            return Response({"error":"The branch already exists"},status=status.HTTP_400_BAD_REQUEST)
        try:
            iscm=User.objects.get(email=cmpemail)
            iscmp=iscm.iscmpid
            company=Company.objects.get(email=cmpemail)
            print("Company exist or not",iscmp)
            if iscmp:
                branch=Branch(branch_id=branch_id,company_id=company,address=branchaddress,pincode=branchpincode,lat=branchlat,long=branchlong)
                branch.save()
                branchdata=Branch.objects.filter(branch_id=branch_id)
                user=User.objects.create_user(email=branch_id,password=branchpassword,branchid=branch,iscmpid=False,isbraid=True,companyid=company)
                return Response({"succes":"Branch is  added to the company"},status=status.HTTP_201_CREATED)
            
            else:
                return Response({"error":"This is not company user id"},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error":"Company matching the provided email does not exist"},status=status.HTTP_404_NOT_FOUND)
        
        # return Response({"Success":"Login successfully"},status=status.HTTP_200_OK)
  
   


# class UserRegisterView(APIView):
#     permission_classes=[IsAuthenticated]
#     def post(self,request):
#         email=request.data.get('email')
#         password=request.data.get('password')

#         pass