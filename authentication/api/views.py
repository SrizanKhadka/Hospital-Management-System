from authentication.models import UserModel
from authentication.models import UserModel
from .serializers import EmailVerificationSerializer
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from authentication.models import *
import jwt
from authentication.api.serializers import (
    UserSerializer,
    LoginSerializer,
    EmailVerificationSerializer,
)
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from utils.permissions import IsAdmin
from rest_framework import status, response
from rest_framework.decorators import action
from utils.EmailThread import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView


class RegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    # this will ensure that only the post method is allowed for this view.
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        data = request.data
        role = data.get("role")

        if role == "ADMIN":
            return self.create_admin(request=request)

        elif role in ["DOCTOR", "STAFF"]:
            return self.create_doctor_or_staff(request=request)

        elif role == "USER":
            return self.create_account(data=data, request=request)

        else:
            return Response(
                {"error": f"Invalid role '{role}' specified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        return serializer.save()

    def create_account(self, data, request):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        print(f"ROLE = {data['role']}")
        self.create_role_specific_account(user=user, role=data["role"])
        self.sendEmailVerification(user, request)
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
        return self.create_account(request.data, request=request)

    def create_doctor_or_staff(self, request):
        if IsAdmin().has_permission(request, self):
            return self.create_account(request.data, request=request)
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

    def sendEmailVerification(self, user, request):
        user_email = UserModel.objects.get(email=user.email)
        tokens = RefreshToken.for_user(user_email).access_token
        # current_site = get_current_site(request).domain
        relative_link = reverse("email-verify")
        path = f"{relative_link}?token={tokens}"
        url = self.request.build_absolute_uri(path)

        print(f'ABOSOULTE URL = {url}')

        email_body = (
            "Hi "
            + user.username
            + " Use the link below to verify your email \n"
            + url
        )
        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email",
        }

        Util.send_email(data=data)

    @action(
        detail=True,
        methods=["POST"],
        url_path="update_profile",
        permission_classes=[permissions.IsAuthenticated],
    )
    def updateProfile(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        print(f"METHOD FROM THE REQUEST = {request.method}")
        print(f"DATA FROM REQUEST = {data}")

        # List of fields that can be updated
        # updatable_fields = ['username', 'fullName', 'email', 'phoneNumber', 'gender','bloodGroup', 'dob', 'address', 'profilePicture']

        # for field in updatable_fields:
        #     if field in data:
        #         # settr() function dynamically sets the value of an attribute on the instance object
        #         setattr(instance, field, data[field])

        # 'partial=True' allows for partial updates
        serializer = self.get_serializer(instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class VerifyEmail(GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        accept = request.headers.get('Accept', '')

        def html_response(message, status_code=status.HTTP_200_OK):
            return HttpResponse(f"<h1>{message}</h1>", content_type="text/html", status=status_code)

        def json_response(message, status_code=status.HTTP_200_OK):
            return Response({"email": message}, status=status_code)

        def respond(message, html_message, status_code=status.HTTP_200_OK):
            if "text/html" in accept:
                return html_response(html_message, status_code)
            return json_response(message, status_code)

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            user = UserModel.objects.get(id=payload["user_id"])

            if user.is_verified:
                return respond("Already verified", "Email Already Verified!")

            user.is_verified = True
            user.save()
            return respond("Successfully activated", "Email Successfully Activated!")

        except jwt.ExpiredSignatureError:
            return respond("Activation Expired", "Activation Expired", status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return respond("Invalid token", "Invalid token", status.HTTP_400_BAD_REQUEST)
