from django.db import models
from django.contrib.auth.models import AbstractUser

# Model for users.

class UserModel(AbstractUser):
    role = models.CharField(max_length=20, default="user")
    fullName = models.CharField(max_length=20)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=15)
    gender = models.CharField(max_length=20)
    bloodGroup = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=18)
    confirmPassword = models.CharField(max_length=18)

    def __str__(self):
        return self.fullName
