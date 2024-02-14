from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Company,User,Branch,OTP
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from . serializer import UserSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from sendingemail import send_email
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
        user=User.objects.create_user(email=email,password=password,iscmpid=True,companyid=company,isadduser=True)
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
                user=User.objects.create_user(email=branch_id,password=branchpassword,branchid=branch,iscmpid=False,isbraid=True,companyid=company,isadduser=True)
                return Response({"succes":"Branch is  added to the company"},status=status.HTTP_201_CREATED)
            
            
            else:
                return Response({"error":"This is not company user id"},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error":"Company matching the provided email does not exist"},status=status.HTTP_404_NOT_FOUND)
        
        # return Response({"Success":"Login successfully"},status=status.HTTP_200_OK)
  
   
class UserRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        fname = data.get('fname')
        lname = data.get('lname')
        cmpid = data.get('cmpid')
        branchid = data.get('branchid')
        requestid = data.get('requestid')

        if not all([email, password, fname, lname, cmpid, branchid, requestid]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            company = Company.objects.get(email=cmpid)
            branch = Branch.objects.get(branch_id=branchid)
            user = User.objects.get(email=requestid)
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        if User.objects.filter(email=email).exists():
            return Response({"error": "The User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.isadduser:
            return Response({"error": "User is not allowed to add new user"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.create_user(email=email, password=password, fname=fname, lname=lname, branchid=branch, companyid=company)
            return Response({"message": "User is created"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
        

        if User.objects.filter(email=email).exists():
            return Response({"error":"The User already exists"},status=status.HTTP_400_BAD_REQUEST)
        try:
            userallow=User.objects.get(email=requestid)
            isuserallow=userallow.isadduser
            print(isuserallow)
        except ObjectDoesNotExist:
            return Response({"error": "User with requestid does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if isuserallow:
            user=User.objects.create_user(email=email,password=password,fname=fname,lname=lname,branchid=branch,companyid=company)
            return Response({"message":"User is created"},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"User is not allowed to add new user"},status=status.HTTP_304_NOT_MODIFIED)
        
class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        oldpassword=request.data.get('oldpassword')
        newpassword=request.data.get('newpassword')
        if not oldpassword or not newpassword:
            return Response({"error":"old password or new password is not provided"},status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(oldpassword):
            return Response({"error":"Current password is incorrect"},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(newpassword)
        user.save()
        update_session_auth_hash(request,user)
        return Response({"message":"password reset successful"},status=status.HTTP_200_OK)
    
class generateotpview(APIView):
    def post(self,request):
        email=request.data.get('email')

        if not email:
            return Response({"error":"Email is required"},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=User.objects.get(email=email)
        except:
            return Response({"error":"user is not found"},status=status.HTTP_404_NOT_FOUND)
        
        
        otp=OTP.generate_otp(email=email)
       

        subject="The otp for Forgot password"
        message="Your otp is "+" "+ otp+". OTP expires in 5 minutes"

        
        send_email(subject,email,message)

        return Response({"isotpsent":True},status=status.HTTP_200_OK)
    
class verityotp(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp_entered=request.data.get('otp')

        if not email or not otp_entered:
            return Response({"error":"email or otp is required to verify"},status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance=OTP.objects.get(email=email,otp=otp_entered)
            if otp_instance.used:
                return Response({"error":"otp is expired"},status=status.HTTP_400_BAD_REQUEST)
            elif otp_instance.is_expired():
                return Response({"error":"OTP has been already been used"})
            
        except OTP.DoesNotExist:
            return Response({"error":"invalid otp or otp has expired","isotpverified":False},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":"OTP verifiec successfully","isotpverified":True},status=status.HTTP_200_OK)


class forgotpasswordview(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp_entered=request.get('otp')
        password=request.data.get('password')

        if not email or not otp_entered or not password:
            return Response({"error":"Invalid OTP or email"})
        
        try:
            otp_obj=OTP.objects.get(email=email,otp=otp_entered,used=False)
            if otp_obj.is_expired():
                return Response({"error":"Invalid OTP or OTP has expired"})
            
        except OTP.DoesNotExist:
            return Response({"error":"Invalid OTP "},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user=User.objects.get(email)
            user.set_password(password)
            user.save()
            otp_obj.used=True
            otp_obj.save()
            return Response({"message":"Password reset sucessfully","ispasswordreset":True},status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error":"user not found","ispasswordreset":False},status=status.HTTP_404_NOT_FOUND)