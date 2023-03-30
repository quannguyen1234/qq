from django.db import models
from apps.User.models import Doctor,BaseUser
from core.references import ImageEnum 
import uuid
# Create your models here.


class HospitalDepartment(models.Model):

    class Meta:
        db_table="HospitalDepartment"

    de_id=models.CharField(primary_key=True,max_length=8)
    name=models.CharField(null=False,max_length=255)
    doctors=models.ManyToManyField(Doctor,through='DoctorDepartment',related_name='departments')


class DoctorDepartment(models.Model):
    do_de_id=models.CharField(primary_key=True,max_length=16)
    de=models.ForeignKey(HospitalDepartment,on_delete=models.CASCADE,null=False)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=False)
    
   

class Image(models.Model):
    
    class Meta:
        db_table="Image"
    
    image_id=models.CharField(primary_key=True,max_length=8,default=uuid.uuid4)
    name=models.CharField(max_length=20,null=True)
    url=models.TextField(null=True)
    base_user=models.ForeignKey(BaseUser,on_delete=models.CASCADE,null=True,related_name='images')
    image_type=models.IntegerField(max_length=60,choices=ImageEnum.__tupple__(),null=True)
    