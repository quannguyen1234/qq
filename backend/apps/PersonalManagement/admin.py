from django.contrib import admin
from .models import HospitalDepartment,DoctorDepartment,Image
# Register your models here.

admin.site.register(HospitalDepartment)
admin.site.register(DoctorDepartment)
admin.site.register(Image)
