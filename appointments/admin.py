from django.contrib import admin
from appointments.models import AppointmentModel,TestAndResultModel
# Register your models here.

admin.site.register(AppointmentModel)
admin.site.register(TestAndResultModel)

