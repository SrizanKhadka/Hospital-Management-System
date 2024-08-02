from django.db import models
from django.contrib.auth.models import AbstractUser

# Choices for fields
ROLE_CHOICES = [
    ("USER", "user"),
    ("ADMIN", "admin"),
    ("DOCTOR", "doctor"),
    ("STAFF", "staff"),
]

GENDER_CHOICES = [
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
]

BLOOD_GROUP_CHOICES = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
]


class UserModel(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    fullName = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phoneNumber = models.CharField(max_length=15)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    bloodGroup = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    dob = models.DateField()
    address = models.CharField(max_length=100)
    shortBio = models.TextField(null=True, blank=True)
    joined_date = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=128)  # Max length for hashed passwords
    confirmPassword = models.CharField(max_length=128)

    # For staff
    jobTitle = models.CharField(max_length=100, null=True, blank=True)

    # For both doctor and Staff
    # schedule = models.CharField(max_length=100, null=True, blank=True)
    schedule = models.JSONField(null=True,blank=True)

    # Doctor specfic fields
    specialization = models.CharField(max_length=100, null=True, blank=True)
    max_appointments_per_day = models.IntegerField(default=8, null=True, blank=True)
    available_days = models.IntegerField(null=True, blank=True)
    consultation_fees = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "fullName",
        "phoneNumber",
        "gender",
        "bloodGroup",
        "dob",
        "address",
    ]

    def __str__(self):
        return self.fullName


class PatientModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Patient - {self.user.fullName}"


class DoctorModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Doctor - {self.user.fullName}"


class StaffModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Staff - {self.user.fullName}"


class AdminModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin - {self.user.fullName}"
