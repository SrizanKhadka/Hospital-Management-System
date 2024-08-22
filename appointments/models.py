from django.db import models
from HMS.choices import StatusChoices
from authentication.models import DoctorModel, PatientModel

# Create your models here.

status = [
    ("PENDING", "Pending"),
    ("CONFIRMED", "Confirmed"),
    ("CANCELLED", "Cancelled"),
    ("REJECTED", "Rejected"),  # only admin can reject the appointments
    ("COMPLETED", "Completed"),
]


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
        max_length=30, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    Consulting_fees_paid_token = models.CharField(max_length=30, unique=True)
    remarks = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment - {self.doctor.user.fullName} - {self.user_patient.user.fullName}"
