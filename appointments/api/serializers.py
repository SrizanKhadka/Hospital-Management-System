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
        doctor = data['doctor']
        print(f'VALIDATE DATA = {doctor.id}')
        self.validate_appointment_date(data=data,doctorId=doctor.id)
        return data

    def validate_appointment_date(self, data, doctorId):
        doctor = data['doctor']
        
        # Fetching the doctor's schedule
        doctor_instance = DoctorModel.objects.get(id=doctor.id)
        schedule = doctor_instance.schedule  # Assuming `schedule` is a JSONField

        # appointment_datetime = data.get("appointment_date")
        # if not appointment_datetime:
        #     raise serializers.ValidationError("Appointment date is required.")

        # appointment_day = appointment_datetime.strftime(
        #     "%A"
        # )  # Get day name (e.g., "Monday")
        # appointment_time = appointment_datetime.time()

        # if appointment_day not in schedule:
        #     raise serializers.ValidationError(
        #         f"Doctor is not available on {appointment_day}s."
        #     )

        # time_slots = schedule[appointment_day]
        # for time_slot in time_slots:
        #     start_time, end_time = time_slot.split("-")
        #     start_time = datetime.strptime(start_time, "%H:%M").time()
        #     end_time = datetime.strptime(end_time, "%H:%M").time()
        #     if start_time <= appointment_time <= end_time:
        #         return data

        # raise serializers.ValidationError(
        #     f"Doctor is not available at {appointment_time} on {appointment_day}s."
        # )
