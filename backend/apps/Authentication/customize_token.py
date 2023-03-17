from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.User.references import RELATED_USER
from rest_framework import exceptions, serializers
class CustomizeTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages={**TokenObtainSerializer.default_error_messages,**{'message':'Fail','flag':False}}
    
     
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except:
            raise exceptions.AuthenticationFailed(
                {'message':'No active account found with the given credentials','flag':False}   
            )
            
        try:
            user_type=self.user.user_type
        
            type_user=getattr(self.user,RELATED_USER[user_type])

            user={
                'id':type_user.get_id(),
                'phone_number':self.user.phone_number,
                'gender':self.user.gender,
                'full_name':f"{self.user.surname} {self.user.firstname}",
                'role':self.user.user_type,
                'email':self.user.email
                }
            data['user']=user
            data['flag']=True
        except Exception as e:
            return {'message':'Fail','flag':False}
        return data
    
