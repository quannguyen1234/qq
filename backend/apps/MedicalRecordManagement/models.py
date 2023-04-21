from django.db import models
import uuid
# Create your models here.
class MedicalRecord(models):
    class Meta:
        db_table="MedicalRecord"

    record_id=models.CharField(primary_key=True,max_length=36,default=uuid.uuid4)
    symptom=models.TextField(null=False)
    diagnosis=models.TextField(null=False)
    treatment_plan=models.TextField(null=False)
    condition=models.TextField(null=False)
    date=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)

# class Prescription(models):
    