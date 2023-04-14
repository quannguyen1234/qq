from django.db import models
from apps.User.models import Doctor,BaseUser
from core.references import ImageEnum,AddressEnum
import uuid
# Create your models here.


class HospitalDepartment(models.Model):

    class Meta:
        db_table="HospitalDepartment"

    de_id=models.CharField(primary_key=True,max_length=36,default=uuid.uuid4)
    name=models.CharField(null=False,max_length=255)
    doctors=models.ManyToManyField(Doctor,through='DoctorDepartment',related_name='departments')

    def __str__(self) -> str:
        return self.name

class DoctorDepartment(models.Model):
    do_de_id=models.CharField(primary_key=True,max_length=36,default=uuid.uuid4)
    de=models.ForeignKey(HospitalDepartment,on_delete=models.CASCADE,null=False)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=False)
    


class Image(models.Model):
    
    class Meta:
        abstract=True

    image_id=models.CharField(primary_key=True,max_length=36,default=uuid.uuid4)
    name=models.CharField(max_length=255,null=True,unique=True)
    url=models.TextField(null=True)
    image_type=models.IntegerField(max_length=60,choices=ImageEnum.__tupple__(),null=True)

class ImageUser(Image):
    
    class Meta:
        db_table="ImageUser"
    
    base_user=models.ForeignKey(BaseUser,on_delete=models.CASCADE,null=True,related_name='images')


class ImageDepartment(Image):
    
    class Meta:
        db_table="ImageDepartment"
    
    department=models.ForeignKey(HospitalDepartment,on_delete=models.CASCADE,null=True,related_name='images')
   
    
class Address(models.Model):
    address_id=models.CharField(primary_key=True,max_length=36,default=uuid.uuid4)
    street=models.CharField(max_length=255)
    village=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    date=models.DateTimeField(auto_now=True)
    base_user=models.ForeignKey(BaseUser,on_delete=models.CASCADE,null=True,related_name='addresses',
                                related_query_name='address'
                                )
    address_type=models.IntegerField(max_length=60,choices=AddressEnum.__tupple__(),null=True)
    
    @property
    def full_address(self):
        return f"{self.street},{self.village},{self.district},{self.city}"