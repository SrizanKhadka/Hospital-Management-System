from rest_framework import serializers
from appointments.models import AppointmentModel
from authentication.models import DoctorModel
import datetime
import json


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentModel
        fields = "__all__"

    def validate(self, data):
        print(f'VALIDATE DATA = {data}')
        # self.validate_appointment_date(data)

    def validate_appointment_date(self, data):
        doctor = data["doctor"]
        if not doctor:
         doctor = DoctorModel.objects.get(id=doctor)
         schedule = (
            doctor.schedule
         )  # Assuming `schedule` is stored as JSONField in DoctorModel
         appointment_datetime = data["appointment_date"]
         appointment_day = appointment_datetime.strftime(
            "%A"
         )  # Get day name (e.g., "Monday")
         appointment_time = appointment_datetime.time()
        else:
            raise serializers.ValidationError("Doctor doesn't exist!")

        if appointment_day not in schedule:
            raise serializers.ValidationError(
                f"Doctor is not available on {appointment_day}s."
            )

        time_slots = schedule[appointment_day]
        for time_slot in time_slots:
            start_time, end_time = time_slot.split("-")
            start_time = datetime.datetime.strptime(start_time, "%H:%M").time()
            end_time = datetime.datetime.strptime(end_time, "%H:%M").time()
            if start_time <= appointment_time <= end_time:
                return appointment_datetime

        raise serializers.ValidationError(
            f"Doctor is not available at {appointment_time} on {appointment_day}s."
        )
