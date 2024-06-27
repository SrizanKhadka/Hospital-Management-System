from rest_framework import serializers
from authentication.models import UserModel


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
