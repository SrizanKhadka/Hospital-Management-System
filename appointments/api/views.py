from rest_framework.response import Response
from HMS.choices import StatusChoices
from appointments.models import AppointmentModel
from authentication.models import *
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from appointments.api.serializers import AppointmentSerializer
from rest_framework.decorators import api_view, action


class CreateAppointmentView(ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = AppointmentModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["POST"], url_path="appointment_cancel")
    def perform_cancellation(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = StatusChoices.CANCELLED

        instance.save()
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    # def perform_update(self, serializer):
    #     request = self.request
    #     user_role = UserModel.objects.get(id=request.user.id).role
    #     instance = self.get_object()
    #     print(f"REQUESTED USER ROLE IN UPDATE = {user_role}")

    #     if user_role == "DOCTOR" and IsAppointmentHolderDoctor().has_object_permission(
    #         request, self, instance
    #     ):
    #         instance.remarks = serializer.validated_data.get(
    #             "remarks", instance.remarks
    #         )
    #         instance.save(update_fields=["remarks"])
    #     elif user_role == "USER" and IsAppointmentHolderUser().has_object_permission(
    #         request, self, instance
    #     ):
    #         instance.reason = serializer.validated_data.get(
    #             "reason", instance.reason)
    #         instance.appointment_date = serializer.validated_data.get(
    #             "appointment_date", instance.appointment_date
    #         )
    #         instance.save(update_fields=["reason", "appointment_date"])
    #     elif user_role == "ADMIN":
    #         serializer.save()

    #     else:
    #         print('I AM IN THE ELSE CASE')
    #         raise ValidationError(
    #             {"message": "Unknown Request!"}, status=status.HTTP_400_BAD_REQUEST
    #         )
