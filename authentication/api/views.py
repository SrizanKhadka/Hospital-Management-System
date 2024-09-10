from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import *
from authentication.api.serializers import UserSerializer, LoginSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from utils.permissions import IsAdmin
from rest_framework import status
from rest_framework.decorators import api_view, action


class RegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    # this will ensure that only the post method is allowed for this view.
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        role = data.get("role")

        if role == "ADMIN":
            return self.create_admin(request=request)

        elif role in ["DOCTOR", "STAFF"]:
            return self.create_doctor_or_staff(request=request)

        elif role == "USER":
            return self.create_account(data=data)

        else:
            return Response(
                {"error": f"Invalid role '{role}' specified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create_account(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        print(f"ROLE = {data['role']}")
        self.create_role_specific_account(user=user, role=data["role"])
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def create_admin(self, request):
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superusers can create ADMIN users."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.create_account(request.data)

    def create_doctor_or_staff(self, request):
        if IsAdmin().has_permission(request, self):
            return self.create_account(request.data)
        else:
            return Response(
                {"error": "You do not have permission to create this type of user."},
                status=status.HTTP_403_FORBIDDEN,
            )

    def create_role_specific_account(self, user, role):
        if role == "DOCTOR":
            DoctorModel.objects.create(user=user)
        elif role == "STAFF":
            StaffModel.objects.create(user=user)
        elif role == "USER":
            PatientModel.objects.create(user=user)
        elif role == "ADMIN":
            AdminModel.objects.create(user=user)

    @action(detail=True, methods=["POST"], url_path="update_profile")
    def updateProfile(self, request, *args, **kwargs):
        instance = self.get_object() 
        data = request.data 

        print(f'METHOD FROM THE REQUEST = {request.method}')
        print(f'DATA FROM REQUEST = {data}')

        # List of fields that can be updated
        updatable_fields = ['username', 'fullName', 'email', 'phoneNumber', 'gender','bloodGroup', 'dob', 'address', 'profilePicture']

        for field in updatable_fields:
            if field in data:
                # settr() function dynamically sets the value of an attribute on the instance object
                setattr(instance, field, data[field])

        instance.save() 
        serializer = self.get_serializer(instance)
        return Response(serializer.data) 


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
