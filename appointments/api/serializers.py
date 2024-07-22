from rest_framework import serializers
from models import AppointmentModel

class AppointmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AppointmentModel
        fields = "__all__"
    
    def validate(self, data):
        #Schedule--> Appointment should be request under the doctor's schedule.
        # date
        pass