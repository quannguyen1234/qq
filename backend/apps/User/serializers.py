from .models import BaseUser,Patient,Doctor
from apps.PersonalManagement.models import ImageUser,HospitalDepartment
from apps.PersonalManagement.serializer import AdressSeializer
from apps.PersonalManagement.models import Address
from rest_framework import serializers
from django.db.transaction import atomic
from django.contrib.auth.password_validation import validate_password as validate_password_defaulf
from apps.User.references import REVERSE_USER_TYPE
from abc import ABC
from core.references import AddressEnum
from core.utils import update_image
import uuid,os
from core.references import ImageEnum
class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id','phone_number','email','surname','firstname','surname','full_name','password',
                  'citizen_identification','birth_day','is_active','current_address'
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
    current_address=AdressSeializer(many=False,required=False)
    
    
    
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

class AvatarSerializer(serializers.CharField):
    def to_internal_value(self, data):
        return str(data)
    

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id','degree','current_job','base_user'
                  ,'notarized_images','departments','avatar','name_images']
    
    notarized_images=serializers.ListField(child=serializers.CharField())
    name_images=serializers.JSONField(write_only=True)
    avatar=serializers.CharField(source='base_user.avatar',required=False)
    base_user = BaseUserSerializer()
    departments=HospitalDepartmentSerializer(many=True,read_only=True)
    
    
    def get_is_approved(self,instance):
        return str(instance.is_approved)
    
 
    @atomic
    def create(self, validated_data):
       
        
        notarized_images=validated_data.pop('notarized_images')
        name_images=validated_data.pop('name_images')
        base_user_data = {**validated_data.pop('base_user')} 
    
        if base_user_data.__contains__('current_address'):
            current_address=base_user_data.pop('current_address')
        else:
            current_address=None
    
        if base_user_data.__contains__('avatar'):
            url_avatar=base_user_data.pop('avatar')
        else:
            url_avatar=None 

        # create base user
        instance_base_user=BaseUser.objects.create(**base_user_data,user_type=REVERSE_USER_TYPE['Doctor'],is_active=False)
        instance_base_user.set_password(instance_base_user.password)
        instance_base_user.save()
        
        #create address
        if current_address is not None:
            Address.objects.create(**current_address,base_user=instance_base_user,
                                   address_type=AddressEnum.CurrentAddress.value
            )

        instance=Doctor.objects.create(**validated_data,base_user=instance_base_user)
       
        for index,url in enumerate(notarized_images):
            img_instance=ImageUser.objects.create(
               name=name_images['notarized_images'][index],
               url=url,
               image_type=ImageEnum.DoctorNotarizedImage.value
            )
            instance.base_user.images.add(img_instance)

        if url_avatar is not None:
            img_instance=ImageUser.objects.create(
               name=name_images['avatar'],
               url=url,
               image_type=ImageEnum.Avatar.value
            )
            
            instance.base_user.images.add(img_instance)
        return instance
    



    
  