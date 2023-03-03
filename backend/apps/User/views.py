from .models import BaseUser
from rest_framework import status,response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from .serializers import BaseUserSerializer
class BaseUserAPI(ModelViewSet):
    queryset=BaseUser.objects.all()
    serializer_class=BaseUserSerializer
    permission_classes=[]

    @action(methods=['post'],detail=False,url_path='reset_password/(?P<phone_number>\w+)')
    def reset_password(self,request,phone_number=None):
       
        conditions=request.session.get('exchangeable_password',None)
        if conditions is not None and phone_number is not None:
            print(conditions)
            if phone_number != conditions['phone_number']:
                request.session.__delitem__('exchangeable_password')
                return JsonResponse({'message':'Phone number is not compatiable to sending phone number before'}
                                    ,status=status.HTTP_403_FORBIDDEN)
            
            
            instance=BaseUser.objects.get(phone_number=phone_number)
            data=request.POST
            new_password=data.get('new_password')
            try:
                validate_password(new_password)
            except Exception as e:
                errror=str(e)
                return JsonResponse({
                    'message':'Password dont guarante for confidential','detail':errror},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            instance.set_password(new_password)
            instance.save()
            return JsonResponse({'message':'oke'})
            
            
              
       
    
            


