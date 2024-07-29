from rest_framework.response import Response
from appointments.models import AppointmentModel
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from appointments.api.serializers import AppointmentSerializer


class CreateAppointmentView(ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = AppointmentModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]
