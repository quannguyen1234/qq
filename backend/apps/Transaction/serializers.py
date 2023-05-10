from rest_framework import serializers
from .models import DiagnosticBill ,DiagnosticBillDetail

class DiagnosticBillSerializer(serializers.ModelSerializer):
    class Meta:
        model=DiagnosticBill
        field='__all__'


        