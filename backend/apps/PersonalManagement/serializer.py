from .models import HospitalDepartment,Address,ImageDepartment
from rest_framework import serializers
from django.db.transaction import atomic
from core.utils import update_image,ImageEnum

class DepartmentImageField(serializers.ListField):
    child=serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
class HospitalDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model=HospitalDepartment
        fields=['de_id','name','images','image_names']

    images=DepartmentImageField(write_only=True)
    image_names=serializers.ListField(child=serializers.CharField(),write_only=True)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = self.get_image_urls(instance)
        return representation
    
    def validate_name(self,name):
        list_name=list(HospitalDepartment.objects.values_list('name',flat=True))
        if name in list_name:
            raise serializers.ValidationError("Name have existed") 
        return name
    
    def get_image_urls(self,instance):
        print(instance)
        return list(instance.images.values_list('url',flat=True))
    
    def get_image_names(self,instance):
        return []
    
    # def get_images(self,instance):
    #     return []
    
    @atomic
    def create(self, validated_data):
        
        
        if validated_data.__contains__('images'):
            images=validated_data.pop('images')
            image_names=validated_data.pop('image_names')
        else:
            images=[]
        print(validated_data)
        
        hospital_instance=HospitalDepartment.objects.create(
               **validated_data
        )

        
        for index,url in enumerate(images):
            image_instance=ImageDepartment.objects.create(
                name=image_names[index],
                url=url,
                image_type=ImageEnum.DepartmentImage.value
            )
            hospital_instance.images.add(image_instance)
        
        return hospital_instance

class AdressSeializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        exclude=['address_type','base_user']
        # fields='__all__'