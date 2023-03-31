from .models import HospitalDepartment
from rest_framework import serializers


class HospitalDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model=HospitalDepartment
        exclude=['doctors']
        