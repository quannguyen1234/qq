from rest_framework import serializers
from .models import DiagnosticBill ,DiagnosticBillDetail
from core.references import FEE_DISTANCE
class DiagnosticBillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=DiagnosticBillDetail
        fields=[
            'id','distance','fee_distance_per_one','doctor_fee','total_fee'
        ]
        extra_kwargs = {
            'bill': {'write_only':True },
          
        }
    
    fee_distance_per_one=serializers.SerializerMethodField()

    
    
    def get_fee_distance_per_one(self,instance):
        return FEE_DISTANCE

    
class DiagnosticBillSerializer(serializers.ModelSerializer):
    class Meta:
        model=DiagnosticBill
        fields=[
            'doctor_id','doctor_name','patient_id','patient_name','pay_time','diagnostic_form','detail',
        ]
        
    doctor_id=serializers.CharField(source='doctor.doctor_id')
    doctor_name=serializers.CharField(source='doctor.base_user.get_full_name')
    patient_id=serializers.CharField(source='patient.patient_id')
    patient_name=serializers.CharField(source='patient.base_user.get_full_name',read_only=True)
    detail=DiagnosticBillDetailSerializer()

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)
    
    # def crgfeate(self, validated_data):
        # return DiagnosticBill.objects.first()
    
        # return super().create(validated_data)

        