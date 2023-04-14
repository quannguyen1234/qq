from django.contrib import admin
from .models import HospitalDepartment,DoctorDepartment,ImageUser,Address,ImageDepartment
# Register your models here.

admin.site.register(HospitalDepartment)
admin.site.register(DoctorDepartment)
admin.site.register(ImageDepartment)
admin.site.register(ImageUser)
admin.site.register(Address)
