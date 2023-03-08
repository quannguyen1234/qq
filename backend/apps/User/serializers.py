from .models import BaseUser,Patient
from rest_framework import serializers
from django.db.transaction import atomic
from apps.User.references import REVERSE_USER_TYPE
from django.contrib.auth.password_validation import validate_password as validate_password_defaulf

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ['id','phone_number','email','surname','firstname','surname','full_name','password']
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
    

# class PatientSerializer(serializers.ModelSerializer):
    
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
        instance_base_user=BaseUser.objects.create(**base_user_data,user_type=REVERSE_USER_TYPE['Doctor'])
        instance=Patient.objects.create(**validated_data,base_user=instance_base_user)
        return instance
    
    # @atomic
    # def update(self,instance,validated_data):
    #     base_user_data=validated_data.pop('base_user')
    #     user=instance.base_user
    #     user_serialize=BaseUser(instance=user,user_type=REVERSE_USER_TYPE['Doctor'])
    #     user_serialize.update(user,dict(base_user_data))
    #     return super().update(instance,validated_data)