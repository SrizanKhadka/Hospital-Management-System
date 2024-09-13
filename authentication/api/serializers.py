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

        read_only_fields = [
            'role', 'joined_date', 'shortBio', 'jobTitle', 'schedule',
            'specialization', 'max_appointments_per_day',
            'available_days', 'consultation_fees'
        ]

    def validate(self, data):
        validated_data = super().validate(data)
        # role = validated_data["role"]
        instance = self.instance
        role = data.get("role", getattr(instance, "role", None))

        if role == "DOCTOR":
            if not validated_data["specialization"]:
                raise serializers.ValidationError(
                    "Doctor's Specialization is required!"
                )
            elif not validated_data["available_days"]:
                raise serializers.ValidationError(
                    "Doctor's available days is required!"
                )
            elif not validated_data["consultation_fees"]:
                raise serializers.ValidationError(
                    "Doctor's consulataion fees is required!"
                )

        if role == "STAFF":
            if not validated_data["jobTitle"]:
                raise serializers.ValidationError("Staff's title is required!")

        if role in ["DOCTOR", "ADMIN", "STAFF"]:
            required_fields = ["shortBio", "joined_date", "schedule"]
            for field in required_fields:
                if not validated_data.get(field):
                    raise serializers.ValidationError(
                        f"{field.replace('_', ' ').capitalize()} is required!"
                    )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(
            **validated_data
        )  # creating the instance of the UserModel.

        if password is not None:
            instance.set_password(
                password
                # This is the way of hashing the password not just posting into the database.
            )

        instance.confirmPassword = instance.password

        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        userData = UserSerializer(self.user)
        print(f'USER = {self.user}')
        token = self.get_token(self.user)
        access_token = str(token.access_token)
        refresh_token = str(token)

        return {
            "access_token": access_token,
            "refresh": refresh_token,
            "user_data": userData.data,
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
