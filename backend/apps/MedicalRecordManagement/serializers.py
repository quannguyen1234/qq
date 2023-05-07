from rest_framework import serializers
from .models import Prescription,MedicalRecord
from apps.User.models import Patient
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Prescription
        exclude=['record']
        extra_kwargs = {
            'prescription_id': {'required':False  },
        }

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model=MedicalRecord
        fields=['record_id','name','symptom','diagnosis','treatment_plan','condition','date','prescriptions'
                ,'patient_id','doctor','doctor_id'
                ]
        extra_kwargs = {
            'doctor': {'write_only':True  },
        }

    date=serializers.SerializerMethodField()
    patient_id=serializers.CharField(source='patient.patient_id')
    doctor_id=serializers.SerializerMethodField()

    def get_doctor_id(self,instance):
        return instance.doctor.doctor_id
    
    def validate_patient_id(self, value):
        try:
            patient = Patient.objects.get(patient_id=value)
        except :
            raise serializers.ValidationError("Invalid patient ID")
        return value
    
    prescriptions=PrescriptionSerializer(many=True)
    def get_date(self,instance):
        return f"{instance.date.month}-{instance.date.day}-{instance.date.year}"

    def create(self, validated_data):
      
        patient_id=validated_data.pop('patient')['patient_id']
        patient=Patient.objects.get(patient_id=patient_id)
        doctor=validated_data.pop('doctor')

        prescriptions=[]
        if validated_data.__contains__('prescriptions'):
            prescriptions=validated_data.pop('prescriptions')

        instance=MedicalRecord.objects.create(**validated_data,patient=patient,doctor=doctor)
        for pre in prescriptions:
            pre_instance=Prescription.objects.create(
                medicine_name=pre['medicine_name'],
                note=pre['note'],
                record=instance
            )

        return instance
    
    def update(self, instance, validated_data):
        prescriptions=[]
        if validated_data.__contains__('prescriptions'):
            prescriptions=validated_data.pop('prescriptions')

        super().update(instance=instance,validated_data=validated_data)

        instance.prescriptions.all().delete()
        for pre in prescriptions:
            pre_instance=Prescription.objects.create(
                medicine_name=pre['medicine_name'],
                note=pre['note'],
                record=instance
            )
        return instance
