from .models import BaseUser,Patient
from rest_framework import status,response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password 
from django.contrib.auth.password_validation import validate_password
from .serializers import BaseUserSerializer,PatientSerializer



class BaseUserAPI(ModelViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = []


    @action(methods = ['patch'], detail = False, url_path='change-password')
    def change_password(self,request):       
        request.data._mutable=True 
        old_password=request.data.get('old_password')
        new_password=request.data.get('new_password')
        instance=request.user
    
        if instance.check_password(old_password):
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
            return JsonResponse({
                    'message':'Sucessfully','flag':True},
                    status=status.HTTP_200_OK
            )
        else:
            return JsonResponse({'message':'Old password is not correct','flag':False},status=status.HTTP_400_BAD_REQUEST)
        
    
    @action(methods = ['patch'], detail = False, url_path='reset-password/(?P<phone_number>\w+)')
    def reset_password(self,request,phone_number=None):
       
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
        else:
            return JsonResponse({'message':'Phone number is not compatiable to sending phone number before','flag':False}
                                    ,status=status.HTTP_403_FORBIDDEN)
        

    
    
    

class PatientAPI(ModelViewSet):
    queryset = Patient.objects.all()    
    serializer_class = PatientSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):        
        base_user_data=request.data['base_user']

        patient_id=Patient.generate_patient_id()
        request.data['patient_id']=patient_id
        split_name = base_user_data.pop("full_name").split(' ')
        base_user_data['surname']=split_name[0]
        base_user_data['firstname']=split_name[1]
        
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            dict_error=e.__dict__['detail']
            dict_error['flag']=False
            return JsonResponse({**dict_error},status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data=serializer.data
        data['flag']=True
        return response.Response(data, status=status.HTTP_201_CREATED, headers=headers)

      
       
    
            


