from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.User.references import RELATED_USER
class CustomizeTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
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
        except Exception as e:
            return {'message':'Fail','flag':False}
        return data
    
# class TokenSecurity():
#     def __init__(self,token) -> None:
#         self.token=token
    
#     def check_token(self):


        


# def 
    
