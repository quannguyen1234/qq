from .models import HospitalDepartment,Address
from rest_framework import serializers


class HospitalDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model=HospitalDepartment
        exclude=['doctors']

class AdressSeializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        exclude=['address_type','base_user']
        # fields='__all__'