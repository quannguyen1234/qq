from django.db import models
from apps.User.models import Patient,Doctor
import uuid
# Create your models here.



class MedicalRecord(models.Model):
    class Meta:
        db_table="MedicalRecord"

    record_id=models.CharField(primary_key=True,max_length=36,default=uuid.uuid4)
    name=models.CharField(max_length=128,null=False,default=" ")
    symptom=models.TextField(null=False)
    diagnosis=models.TextField(null=False)
    treatment_plan=models.TextField(null=False)
    condition=models.TextField(null=False)
    date=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='records',null=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='records',null=True)
    
    def __str__(self):
        try:
            return f"Record of Patient: {self.patient.patient_id}"
        except:
            return super().__str__()
    
class Prescription(models.Model):
    class Meta:
        db_table="Prescription"

    prescription_id=models.IntegerField(primary_key=True,auto_created=True)
    medicine_name=models.CharField(max_length=30)
    note=models.TextField(null=True)
    record=models.ForeignKey(MedicalRecord,on_delete=models.CASCADE,null=True,related_name='prescriptions')

    # def __str__(self) -> str:
        # return f"{self.medicine_name}-{self.record.record_id}"



    