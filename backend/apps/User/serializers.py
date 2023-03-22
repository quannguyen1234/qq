from .models import BaseUser,Patient,Doctor
from rest_framework import serializers
from django.db.transaction import atomic
from django.contrib.auth.password_validation import validate_password as validate_password_defaulf
from apps.User.references import REVERSE_USER_TYPE
from abc import ABC
from core.config_outsystems.cfg_firebase import storage,firebase_admin
from django.core.files.storage import default_storage
import uuid,os
class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id','phone_number','email','surname','firstname','surname','full_name','password',
                  'citizen_identification','address','birth_day'
                ]
        extra_kwargs = {
            'id': {'required':False  },
            'firstname' : {'write_only':True},
            'surname' : {'write_only':True},
            'password' : {'write_only':True}
        }
    full_name=serializers.SerializerMethodField()
    
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
        instance_base_user=BaseUser.objects.create(**base_user_data,user_type=REVERSE_USER_TYPE['Patient'])
        instance=Patient.objects.create(**validated_data,base_user=instance_base_user)
        return instance
    
    @atomic
    def update(self,instance,validated_data):
        base_user_data=validated_data.pop('base_user')
        base_user=instance.base_user
        base_user_serializer=BaseUserSerializer(instance=base_user)
        base_user_serializer.update(instance=base_user,validated_data=base_user_data)
        return super().update(instance,validated_data)
    

# class ApprovedField(serializers.Field):

#     def to_representation(self, value):
#         return str(value)
    

class NotarizedimageField(serializers.Field):

    def to_representation(self, instance):
    
        if instance is None:
            return None
        
        return storage.child("images/notarized_image/{}".format(instance)).get_url(firebase_admin['idToken'])
    
    def to_internal_value(self, data):
        return data

def process_image(instance,name,url):
    if instance is not None:
        try:
            storage.delete("{}/{}".format(url,instance.notarized_image),firebase_admin['idToken']) 
        except:
            pass
    instance.notarized_image=name
    
    storage.child("{}/{}".format(url,name)).put("media/"+name)
    
    if os.path.exists("media/"+name):
        os.remove("media/"+name)

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id','degree','current_job','notarized_image','base_user','is_approved']
        extra_kwargs = {
            'is_approved': {'required':False}
        }

    notarized_image=NotarizedimageField()
    is_approved=serializers.SerializerMethodField()
    base_user = BaseUserSerializer()
    
    def get_is_approved(self,instance):
        return str(instance.is_approved)
    
    @atomic
    def create(self, validated_data):

        base_user_data = validated_data.pop('base_user')
        instance_base_user=BaseUser.objects.create(**base_user_data,user_type=REVERSE_USER_TYPE['Doctor'])
        instance=Doctor.objects.create(**validated_data,base_user=instance_base_user)
        process_image(instance,validated_data.get('notarized_image'),'images/notarized_image')

        return instance
    
  