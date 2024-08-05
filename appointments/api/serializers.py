from rest_framework import serializers
from appointments.models import AppointmentModel
from authentication.models import DoctorModel
from datetime import datetime


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppointmentModel
        fields = "__all__"

    def validate(self, data):
        validate_data=super().validate(data)
        self.isMaxAppointmentFilled(data=validate_data)
        self.validate_user(data=validate_data)
        self.validate_date_appointment(data=validate_data)
        return validate_data

    def validate_user(self, data):
        request = self.context.get('request', None)
        print(F'REQUESTED USER = {request.user.id}')
        print(F'USER = {data["user_patient"].id}')
        
        if request == "POST":
         if request and request.user.id == data["user_patient"].user.id:
            return data
         else:
            raise serializers.ValidationError("User is not matching!")
        elif request == "PUT":
            return data

    def validate_date_appointment(self, data):
        print(f"Data type: {type(data)}, Data content: {data}")
        doctor = data["doctor"]
        doctor_instance = DoctorModel.objects.get(id=doctor.id)
        schedule = doctor_instance.user.schedule  # Assuming `schedule` is a JSONField

        appointment_datetime = data.get("appointment_date")
        if not appointment_datetime:
            raise serializers.ValidationError("Appointment date is required.")

        appointment_day = appointment_datetime.strftime(
            "%A"
        )  # Get day name (e.g., "Monday")
        appointment_time = appointment_datetime.time()

        if appointment_day not in schedule:
            raise serializers.ValidationError(
                f"Doctor is not available on {appointment_day}s."
            )

        time_slots = schedule[appointment_day]
        for time_slot in time_slots:
            try:
                start_time_str, end_time_str = time_slot.split("-")
                start_time = datetime.strptime(start_time_str, "%H:%M").time()
                end_time = datetime.strptime(end_time_str, "%H:%M").time()
            except ValueError:
                raise serializers.ValidationError("Invalid time slot format.")

            if start_time <= appointment_time <= end_time:
                return data

        raise serializers.ValidationError(
            f"Doctor is not available at {
                appointment_time} on {appointment_day}s."
        )

    def isMaxAppointmentFilled(self, data):
        appointment_date = data["appointment_date"].date()
        doctor_id = data["doctor"].id

        # Filter appointments for the given doctor on the specified date
        appointments_by_doctor = (
            AppointmentModel.objects.filter(doctor_id=doctor_id)
            .filter(appointment_date__date=appointment_date)
            .count()
        )

        # Debugging prints (placed before the return statement)
        print(f"APPOINTMENT DATE = {appointment_date}")
        print(f"APPOINTMENTS FILTERED BY DOCTOR = {appointments_by_doctor}")

        # Check if the number of appointments exceeds the maximum allowed
        if appointments_by_doctor >= data["doctor"].user.max_appointments_per_day:
            raise serializers.ValidationError(
                "Maximum Appointments per day has been reached."
            )

        return data

    # def validate_appointment_date(self, data):
    #     print(f'Data type: {type(data)}, Data content: {data}')
    # doctor = data['doctor']
    # print(f'DOCTOR WHILE VALIDATING = {doctor.id}')

    # Fetching the doctor's schedule
    # doctor_instance = DoctorModel.objects.get(id=doctor.id)
    # schedule = doctor_instance.schedule  # Assuming `schedule` is a JSONField

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
