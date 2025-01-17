from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from action.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,UserSendRestLinkSerializer,UserResetPasswordSerializer,BooksAndBrochureSerializer,BlogSerializer
from django.contrib.auth import authenticate
from action.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from action.models import BooksAndBrochure,Blog
import json


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
# Create your views here.


class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({"msg":"Registration Success","token":token},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes=[UserRenderer] 
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get("email")
            password=serializer.data.get("password")
            user =authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)         
                return Response({"msg":"Login Successfully!","token":token},status=status.HTTP_200_OK)
            else:
                return Response({"msg":"Login Not Successfully Please Check the details"},status=status.HTTP_400_BAD_REQUEST)
                
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user':request.user}) 
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Change Successfully!"},status=status.HTTP_200_OK)
        else:   
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)   

class UserSendRestLinkView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserSendRestLinkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password reset email has been sent."},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class UserResetPasswordView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,cid,token,format=None):
        serializer=UserResetPasswordSerializer(data=request.data,context={'cid':cid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Change Successfully."},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        




class BooksAndBrochureView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format=None):
        data = json.loads(request.body)
        value=data.get('type')
        books = BooksAndBrochure.objects.filter(type=value)
        serializer = BooksAndBrochureSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class BlogView(APIView):
    renderer_classes=[UserRenderer]
    def get(self, request, format=None):
        blog = Blog.objects.all()
        serializer = BlogSerializer(blog, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
       
    
