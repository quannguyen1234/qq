from django.db import models
from apps.User.models import Patient,Doctor
# Create your models here.
class ConnectDoctor(models.Model):
    # class Meta:
    #     constraints=[
    #         models.UniqueConstraint(fields=['doctor','patient'],name='unique_conversation')
    #     ]
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,unique=True)
    doctor_channel=models.TextField()
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,unique=True)
    patient_channel=models.TextField(null=True)
    is_confirm=models.BooleanField(default=False)
    fee=models.FloatField(default=0)
