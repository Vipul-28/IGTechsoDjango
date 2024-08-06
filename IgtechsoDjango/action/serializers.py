from rest_framework import serializers
from action.models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from action.utils import Util
class   UserRegistrationSerializer(serializers.ModelSerializer):
    # password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','user_name','password']
        extra_kwargs={
            'password':{'write_only':True}
        }
    # def validate(self, attrs):
    #     return attrs
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','user_name','first_name','last_name']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
    def validate(self,attrs):
        password=attrs.get("password")
        password2=attrs.get("password2")
        user=self.context.get('user')
        print("user : ",user)
        if password!=password2:
            raise serializers.ValidationError("password and Confirm password not matches ")
        user.set_password(password)
        user.save()
        return attrs

class UserSendRestLinkSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link="https://localhost:3000/api/user/reset/"+uid+"/"+token
            print("link :-> ",link)
            body="click following link to reset your Password -> "+link
            data={
                'subject':"Reset Your Password !",
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationErr('you are not a valid user ')

class UserResetPasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
    def validate(self,attrs):
        password=attrs.get("password")
        password2=attrs.get("password2")
        if password!=password2:
            raise serializers.ValidationError("password and Confirm password not matches ")
        cid=self.context.get('cid')
        token=self.context.get('token')
        Cid=smart_str(urlsafe_base64_decode(cid))
        user=User.objects.get(id=Cid)
        if not PasswordResetTokenGenerator().check_token(user,token):
           raise ValidationErr({"msg":"Token is not Valid!."})
        user.set_password(password)
        user.save()
        return attrs
