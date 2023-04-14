from .models import HospitalDepartment,Address,ImageDepartment
from rest_framework import serializers
from django.db.transaction import atomic
from core.utils import update_image,ImageEnum

class HospitalDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model=HospitalDepartment
        exclude=['doctors']

    images=serializers.ListField(child=serializers.CharField())
    
    @atomic
    def create(self, validated_data):
        print(validated_data)
        if validated_data.__contains__('images'):
            images=validated_data.pop('images')
        else:
            images=[]

        HospitalDepartment.objects.create(
               **validated_data
        )
        for url in images:
            img_instance=update_image(url,{
                'image_type':ImageEnum.Avatar.value,
            })
            
        raise ValueError("233")
        # return super().create(validated_data)

class AdressSeializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        exclude=['address_type','base_user']
        # fields='__all__'