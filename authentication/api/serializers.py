from rest_framework import serializers
from authentication.models import UserModel
from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        # fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "confirmPassword": {"write_only": True},
        }
        exclude = ("user_permissions", "groups")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model( **validated_data)  # creating the instance of the UserModel.

        if password is not None:
            instance.set_password(password)  # This is the way of hashing the password not just posting into the database.
        instance.save()
        return instance
    
class LoginSerializer(TokenObtainPairSerializer):
    
    def validate(self,attrs):
        attrs = super().validate(attrs)
        userData = UserSerializer(self.user)
        token = self.get_token(self.user)
        access_token = str(token.access_token)
        refresh_token = str(token)
        
        return {
            'access_token': access_token,
            'refresh': refresh_token,
            'user_data': userData.data
        }

# '**validated_data' means unpacking the dictionary
# This is equivalent to of writing like this

#
# instance = self.Meta.model(
#     role='user',
#     fullName='John Doe',
#     email='john.doe@example.com',
#     phoneNumber='123-456-7890',
#     gender='Male',
#     bloodGroup='O+',
#     dob='1990-01-01',
#     address='123 Main St, Anytown, USA'
# )
