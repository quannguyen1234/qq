from rest_framework import serializers
from apps.User.models import Doctor
from core.references import AddressEnum,ImageEnum

class DoctorAppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Doctor
        fields=['doctor_id','full_name','departments','address','avatar']

    full_name=serializers.SerializerMethodField()
    departments=serializers.SerializerMethodField()
    address=serializers.SerializerMethodField()
    avatar=serializers.SerializerMethodField()

    def get_full_name(self,instance):
        return instance.base_user.get_full_name
    
    def get_departments(self,instance):
        
        departments=instance.departments.all()
        dict_de=[]
        for de in departments:
            dict_de.append({
                'id':de.de_id,
                'name':de.name
            })
        return dict_de
        
    def get_address(self,instance):

        return instance.base_user.addresses.get(
            address_type=AddressEnum.CurrentAddress.value
        ).full_address
       
    def get_avatar(self,instance):
        try:
            return instance.base_user.images.get(
                image_type=ImageEnum.Avatar.value
            ).url
        except:
            return None
    

        
    
