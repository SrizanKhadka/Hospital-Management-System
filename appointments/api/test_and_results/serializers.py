from rest_framework import serializers
from appointments.models import TestAndResultModel

class TestAndResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAndResultModel
        fields = "__all__"