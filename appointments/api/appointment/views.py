from rest_framework.response import Response
from HMS.choices import StatusChoices
from appointments.models import AppointmentModel
from authentication.models import *
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from appointments.api.serializers import AppointmentSerializer
from rest_framework.decorators import api_view, action
from authentication.models import PatientModel


class CreateAppointmentView(ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = AppointmentModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user.id
        patient = PatientModel.objects.get(user=user).id

        queryset = queryset.filter(user_patient=patient)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"], url_path="appointment_cancel")
    def perform_cancellation(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = StatusChoices.CANCELLED

        instance.save()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)