from rest_framework import serializers
from .models import Prescription,MedicalRecord

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Prescription
        exclude=['record']
        
class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicalRecord
        fields=['record_id','symptom','diagnosis','treatment_plan','condition','date','prescriptions']

    date=serializers.SerializerMethodField()
    prescriptions=PrescriptionSerializer(many=True)
    def get_date(self,instance):
        return f"{instance.date.month}-{instance.date.day}-{instance.date.year}"

    # c=PrescriptionSerializer()

    

