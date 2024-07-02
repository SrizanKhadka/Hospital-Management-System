from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import UserModel
from authentication.api.serializers import UserSerializer, LoginSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.api.permissions import IsAdmin
from rest_framework import status
from rest_framework import serializers


class RegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def create(self, request, *args, **kwargs):
        role = request.data.get("role")
        user = request.user

        if role == "ADMIN":
            if not user.is_superuser:
                return Response(
                    {"error": "Only superusers can create ADMIN users."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            else:
                return self.create_account(request.data)

        elif role in ["DOCTOR", "STAFF"]:
            if IsAdmin().has_permission(request, self):
                return self.create_account(request.data)
            else:
                return Response(
                    {
                        "error": "You do not have permission to create this type of user."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        elif role == "USER":
            return self.create_account(request.data)

        else:
            return Response(
                {"error": f"Invalid role '{role}' specified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        serializer.save()

    def create_account(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
