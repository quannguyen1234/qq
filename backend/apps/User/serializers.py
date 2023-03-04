from .models import BaseUser
from rest_framework import serializers

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = '__all__'

# class PatientSerializer(serializers.ModelSerializer):
    