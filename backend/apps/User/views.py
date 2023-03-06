from .models import BaseUser,Patient
from rest_framework import status,response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from .serializers import BaseUserSerializer,PatientSerializer
class BaseUserAPI(ModelViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = []

    @action(methods = ['patch'], detail = False, url_path='change-password/(?P<phone_number>\w+)')
    def change_password(self,request,phone_number=None):
       
        conditions=request.session.get('exchangeable_password',None)
        if conditions is not None and phone_number is not None:
            if phone_number != conditions['phone_number']:
                request.session.__delitem__('exchangeable_password')
                return JsonResponse({'message':'Phone number is not compatiable to sending phone number before','flag':False}
                                    ,status=status.HTTP_403_FORBIDDEN)
            
            
            instance=BaseUser.objects.get(phone_number=phone_number)
            data=request.POST
            new_password=data.get('new_password')
            try:
                validate_password(new_password)
            except Exception as e:
                errror=str(e)
                return JsonResponse({
                    'message':'Password dont guarante for confidential','detail':errror,'flag':False},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            instance.set_password(new_password)
            instance.save()
            return JsonResponse({'message':'successfully','flag':True})
    
class PatientAPI(ModelViewSet):
    queryset = Patient.objects.all()    
    serializer_class = PatientSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        base_user_data=request.data['base_user']
        split_name = base_user_data.pop("full_name").split(' ')
        base_user_data['surname']=split_name[0]
        base_user_data['firstname']=split_name[1]
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data=serializer.data
        data['flag']=True
        return response.Response(data, status=status.HTTP_201_CREATED, headers=headers)

      
       
    
            


