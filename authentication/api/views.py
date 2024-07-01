from rest_framework.views import APIView
from authentication.models import UserModel
from authentication.api.serializers import UserSerializer, LoginSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView



class RegistrationView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = [permissions.AllowAny]

class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    
