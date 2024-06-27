from rest_framework.views import APIView
from authentication.models import UserModel
from authentication.api.serializers import UserSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class RegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = [permissions.AllowAny]
