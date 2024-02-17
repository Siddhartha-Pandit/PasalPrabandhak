from . import sendingemail
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . models import Company,User,Branch,OTP,attandance
from django.contrib.auth import authenticate,login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from . serializer import UserSerializer,BranchListSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash

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
        user=User.objects.create_user(email=email,password=password,iscmpid=True,companyid=company,isadduser=True,isdeletecompany=True,isedituser=True,iseditbranch=True,isaddbranch=True)
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
        cmpuser=request.user
        branch_id=request.data.get('branch_id')
        branchpassword=request.data.get('branchpassword')
        branchaddress=request.data.get('branchaddress')
        branchpincode=request.data.get('pincode')
        branchlat=request.data.get('lat')
        branchlong=request.data.get('long')

        if not  branchpassword or not branchaddress or not branchpincode or not branchlat or not branchlong:
            return Response({"error":"All the data is not provided please provide all data"},status=status.HTTP_400_BAD_REQUEST)
        
        if Branch.objects.filter(branch_id=branch_id).exists():
            return Response({"error":"The branch already exists"},status=status.HTTP_400_BAD_REQUEST)
        try:
          
            iscmp=cmpuser.isaddbranch
            print("iscmp",iscmp)
            
            if iscmp:
                branch=Branch(branch_id=branch_id,company_id=cmpuser.companyid,address=branchaddress,pincode=branchpincode,lat=branchlat,long=branchlong)
                branch.save()
                branchdata=Branch.objects.filter(branch_id=branch_id)
                user=User.objects.create_user(email=branch_id,password=branchpassword,branchid=branch,iscmpid=False,isbraid=True,companyid=cmpuser.companyid,isadduser=True)
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
       
        branchid = data.get('branchid')
       
        requsr=request.user
        if not all([email, password, fname, lname,  branchid]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            branch = Branch.objects.get(branch_id=branchid)
            
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        if User.objects.filter(email=email).exists():
            return Response({"error": "The User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if not requsr.isadduser:
            return Response({"error": "User is not allowed to add new user"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.create_user(email=email, password=password, fname=fname, lname=lname, branchid=branch, companyid=requsr.companyid)
            return Response({"message": "User is created"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
        

   
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
        message="Your otp is "+" "+ str(otp.otp)+". OTP expires in 5 minutes"

        
        sendingemail.send_email(subject,email,message)

        return Response({"isotpsent":True},status=status.HTTP_200_OK)
    
class verityotp(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp_entered=request.data.get('otp')

        if not email or not otp_entered:
            return Response({"error":"email or otp is required to verify"},status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_instance=OTP.objects.get(user=email,otp=otp_entered)
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
        otp_entered=request.data.get('otp')
        password=request.data.get('password')

        if not email or not otp_entered or not password:
            return Response({"error":"Invalid OTP or email"})
        
        try:
            user=User.objects.get(email=email)
            otp_obj=OTP.objects.get(user=user,otp=otp_entered,used=False)
            if otp_obj.is_expired():
                return Response({"error":"Invalid OTP or OTP has expired"})
            
            user.set_password(password)
            user.save()
            otp_obj.used=True
            otp_obj.save()
            return Response({"message":"Password reset sucessfully","ispasswordreset":True},status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error":"User not found"},status=status.HTTP_404_NOT_FOUND)
        except OTP.DoesNotExist:
            return  Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
       
class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        logout(request)
        return Response({"message":"user logout successfully"},status=status.HTTP_200_OK)

class AttendanceView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        email=request.data.get('email')
        if not email:
            return Response({"error":"email is required"})
        
        try:
           
           
            user=request.user
            company=user.companyid 
            branch=user.branchid
            current_date=timezone.now().date()
            already_marked=attandance.objects.filter(userid=user,time__date=current_date,company_id=company,branch_id=branch).exists() 
            if already_marked:
                return Response({"error": "Attendance already marked for today"}, status=status.HTTP_400_BAD_REQUEST)
            ipaddress=request.META.get('REMOTE_ADDR')
            if user.istakeattendance:
                attendance=attandance.objects.create(userid=user,time=datetime.now(),company_id=company, branch_id=branch,ipaddress=ipaddress)
            return Response({"message":"Attendance is recorded","isattendancemarked":True},status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"message":"user not found","isattendancemarked":False},status=status.HTTP_404_NOT_FOUND)

# https://ipapi.co/103.152.114.114/json/
        
class BranchAllList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        print("user belong to company id",user.email)
        try:
            if  not user.isviewbranch:
                  return Response({"error":"You are not allowed to view the data"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            branch=Branch.objects.filter(company_id=user.email)
            serializer=BranchListSerializer(branch,many=True)
            
            #      searilizer=CustomerSerializers(customer,many=True)
            # customer=Customer.objects.filter(companyid=user.companyid)
            return Response({"message":serializer.data})
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BranchDetailList(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        email=request.data.get('email')
        print("user belong to company id",user.email)
        try:
            if user.iscmpid:
                if not email:
                    return Response({"error":"email is required"},status=status.HTTP_400_BAD_REQUEST)
                if not Branch.objects.filter(branch_id=email,company_id=user.companyid).exists():
                    return Response({"error":"The branch does not exists is required"},status=status.HTTP_404_NOT_FOUND)

                branch=Branch.objects.filter(branch_id=email,company_id=user.companyid)
            elif user.isbraid:
                branch=Branch.objects.filter(branch_id=user.email,company_id=user.companyid)
            else:
                return Response({"error":"You are not allowed to access the user data"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            

            serializer=BranchListSerializer(branch,many=True)
            
            #      searilizer=CustomerSerializers(customer,many=True)
            # customer=Customer.objects.filter(companyid=user.companyid)
            return Response({"message":serializer.data})
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserAllListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        email=request.data.get('email')
        
        print("user belong to company id",user.email)
        try:
            if user.iscmpid:
                if not email:
                    return Response({"error":"email is required"},status=status.HTTP_400_BAD_REQUEST)
                if not Branch.objects.filter(branch_id=email,company_id=user.companyid).exists():
                    return Response({"error":"The branch does not exists is required"},status=status.HTTP_404_NOT_FOUND)

                userdata=User.objects.filter(companyid=user.companyid,branchid=email)
                
            elif user.isbraid:
                

                userdata=User.objects.filter(companyid=user.companyid,branchid=user.branchid)
            
            else:
                return Response({"error":"You are not allowed to access the user data"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            serializer=UserSerializer(userdata,many=True)


            #      searilizer=CustomerSerializers(customer,many=True)
            # customer=Customer.objects.filter(companyid=user.companyid)
            return Response({"message":serializer.data})
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserAllDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        email=request.data.get('email')
        
        
        print("user belong to company id",user.email)
        try:
            if user.iscmpid:
                if not email:
                    return Response({"error":"email is required"},status=status.HTTP_400_BAD_REQUEST)
                if not User.objects.filter(email=email,companyid=user.companyid).exists():
                    return Response({"error":"The branch does not exists"},status=status.HTTP_404_NOT_FOUND)

                userdata=User.objects.filter(companyid=user.companyid,email=email)
                
            elif user.isbraid:
                

                userdata=User.objects.filter(email=email,companyid=user.companyid,branchid=user.branchid)
            
            else:
                return Response({"error":"You are not allowed to access the user data"},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            serializer=UserSerializer(userdata,many=True)


            #      searilizer=CustomerSerializers(customer,many=True)
            # customer=Customer.objects.filter(companyid=user.companyid)
            return Response({"message":serializer.data})
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class EditBranchView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data
        branch_id = data.get("branch_id")

        try:
            if not user.iseditbranch:
                return Response({"error": "You are not allowed to edit the branch"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

            # Retrieve the Branch object using correct field name
            branch = Branch.objects.get(branch_id=branch_id, company_id=user.companyid)
            # Retrieve the related User object
            branchdata = User.objects.get(email=branch_id, companyid=user.companyid)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Create serializer instances with the retrieved objects and request data
        branchserializer = BranchListSerializer(branch, data=data)
        userserializer = UserSerializer(branchdata, data=data)
        
        # Validate the serializer data
        if branchserializer.is_valid() and userserializer.is_valid():
            # Save the updated data
            branchserializer.save()
            userserializer.save()
            
            return Response({"message": "Branch and User data updated successfully"}, status=status.HTTP_200_OK)
        else:
            # Return errors if the data is not valid
            return Response({
                "branch_errors": branchserializer.errors if not branchserializer.is_valid() else None,
                "user_errors": userserializer.errors if not userserializer.is_valid() else None
            }, status=status.HTTP_400_BAD_REQUEST)
        
class EditUserView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request):
        user=request.user
        email=request.data.get("email")
        try:
            if not user.isedituser:
                 return Response({"error":"You are not allowed to edit the branch",},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
            userdata=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"Branch not found",},status=status.HTTP_404_NOT_FOUND)
        
        serializer=UserSerializer(userdata,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class DeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        req_user = request.user
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.iscmpid:
            if not req_user.isdeletecompany:
                return Response({"error": "Not allowed to delete company"}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                company = Company.objects.get(email=email)
                company.delete()
                return Response({"message": "Company deleted successfully"}, status=status.HTTP_200_OK)
            except Company.DoesNotExist:
                return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        elif user.isbraid:
            if not req_user.isdeletebranch:
                return Response({"error": "Not allowed to delete branch"}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                branch = Branch.objects.get(branch_id=email)
                branch.delete()
                return Response({"message": "Branch deleted successfully"}, status=status.HTTP_200_OK)
            except Branch.DoesNotExist:
                return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)

        else:
            if not req_user.isdeleteuser:
                return Response({"error": "Not allowed to delete user"}, status=status.HTTP_403_FORBIDDEN)
            
            try:
                user = User.objects.get(email=email)
                user.delete()
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)