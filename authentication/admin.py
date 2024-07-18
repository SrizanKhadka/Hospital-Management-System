from django.contrib import admin
from authentication.models import *

# Register your models here.

admin.site.register(UserModel)
admin.site.register(DoctorModel)
admin.site.register(PatientModel)
admin.site.register(AdminModel)
admin.site.register(StaffModel)