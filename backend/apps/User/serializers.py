from .models import BaseUser,Patient,Doctor
from apps.PersonalManagement.models import Image,HospitalDepartment
from rest_framework import serializers
from django.db.transaction import atomic
from django.contrib.auth.password_validation import validate_password as validate_password_defaulf
from apps.User.references import REVERSE_USER_TYPE
from abc import ABC

import uuid,os
from core.references import ImageEnum
class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id','phone_number','email','surname','firstname','surname','full_name','password',
                  'citizen_identification','address','birth_day','is_active'
                ]   
        extra_kwargs = {
            'id': {'required':False  },
            'firstname' : {'write_only':True},
            'surname' : {'write_only':True},
            'password' : {'write_only':True},
            'is_active':{'read_only':True}
        }
        
    birth_day=serializers.DateField(input_formats=['%m-%d-%Y'])
    full_name=serializers.SerializerMethodField()
    is_active=serializers.SerializerMethodField()
    
    def get_is_active(self,instance):
        return instance.is_active
        
    def get_full_name(self,instance):
        return instance.surname + ' ' + instance.firstname

    def validate_password(self,value):
        validate_password_defaulf(value)
        return value

class FieldHandle:

    def find_field(self):
        current_object_fields=dict(self.fields)
        nested_object_fields=dict(current_object_fields.pop('base_user').fields).keys() #get keys
        current_object_fields=current_object_fields.keys() #get keys
    
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
    base_user = BaseUserSerializer()
    
    
    def validate(self, attrs):
        return super().validate(attrs)

    @atomic
    def create(self, validated_data):
        base_user_data = validated_data.pop('base_user')

        password=base_user_data.pop('password')
        instance_base_user=BaseUser.objects.create(**base_user_data,user_type=REVERSE_USER_TYPE['Patient'])
        instance_base_user.set_password(password)
        instance_base_user.save()
        instance=Patient.objects.create(**validated_data,base_user=instance_base_user)
        return instance
    
    @atomic
    def update(self,instance,validated_data):
        base_user_data=validated_data.pop('base_user')

        base_user=instance.base_user
        base_user_serializer=BaseUserSerializer(instance=base_user)
        base_user_serializer.update(instance=base_user,validated_data=base_user_data)

        if base_user_data.__contains__('password'):
            base_user_data.set_password(base_user_data.password)
            base_user_data.save()
        return super().update(instance,validated_data)
    





class HospitalDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=HospitalDepartment
        exclude=['doctors']

# class DepartmentSerializer(serializers.RelatedField):
#     def to_representation(self, value):
#         return 


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id','degree','current_job','base_user','notarized_images','departments']
    
    notarized_images=serializers.ListField(child=serializers.CharField())
    base_user = BaseUserSerializer()
    departments=HospitalDepartmentSerializer(many=True,read_only=True)
    

    def get_is_approved(self,instance):
        return str(instance.is_approved)
   
    @atomic
    def create(self, validated_data):
        urls=validated_data.pop('notarized_images')
       
        base_user_data = validated_data.pop('base_user')
        instance_base_user=BaseUser.objects.create(**base_user_data,user_type=REVERSE_USER_TYPE['Doctor'],is_active=False)
        instance_base_user.set_password(instance_base_user.password)
        instance_base_user.save()
        
        instance=Doctor.objects.create(**validated_data,base_user=instance_base_user)
        images=Image.objects.filter(url__in=urls)
        for img in images:
            instance.base_user.images.add(img)
        
       
        return instance
    

    
    
  