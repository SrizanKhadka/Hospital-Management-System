from rest_framework import serializers
from appointments.models import TestAndResultModel

class TestAndResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAndResultModel
        fields = "__all__"
    

    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        test_and_result = validated_data["test_type"]
        tests = validated_data["appointment"].tests

        if not test_and_result in tests:
            raise serializers.ValidationError(
                f"{test_and_result} is not recommended in the appointment.")

        return validated_data
