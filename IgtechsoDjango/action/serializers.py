from rest_framework import serializers
from action.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
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