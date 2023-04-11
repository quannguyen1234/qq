from django.db import models
from apps.User.models import Patient,Doctor
# Create your models here.
class ConnectDoctor(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    doctor_channel=models.TextField()
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True)
    patient_channel=models.TextField(null=True)
    is_confirm=models.BooleanField(default=False)