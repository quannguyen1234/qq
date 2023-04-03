from django.contrib import admin
from .models import HospitalDepartment,DoctorDepartment,Image,Address
# Register your models here.

admin.site.register(HospitalDepartment)
admin.site.register(DoctorDepartment)
admin.site.register(Image)
admin.site.register(Address)
