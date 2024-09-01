from django.db import models
from HMS.choices import StatusChoices
from authentication.models import DoctorModel, PatientModel
from HMS.choices import TestTypes


class AppointmentModel(models.Model):
    doctor = models.ForeignKey(
        DoctorModel, on_delete=models.CASCADE, related_name="appointments"
    )
    user_patient = models.ForeignKey(
        PatientModel, on_delete=models.CASCADE, related_name="appointments"
    )
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=30, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    Consulting_fees_paid_token = models.CharField(max_length=30, unique=True)
    tests_required = models.CharField(
        max_length=30, choices=TestTypes, null=True, blank=True
    )
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment - {self.doctor.user.fullName} - {self.user_patient.user.fullName}"


class TestAndResultModel(models.Model):
    appointment = models.ForeignKey(
        AppointmentModel, on_delete=models.CASCADE, related_name="appointment_test"
    )
    test_type = models.CharField(max_length=100, choices=TestTypes)
    test_name = models.CharField(max_length=100)
    test_fees_paid_token = models.CharField(max_length=30, unique=True)
    test_date = models.DateTimeField(auto_now_add=True)
    test_result_available = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    report_file = models.FileField(
        upload_to="test_reports/", null=True, blank=True
    )  # Upload related file
