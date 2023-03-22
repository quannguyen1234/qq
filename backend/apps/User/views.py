from .models import BaseUser,Patient,Doctor
from rest_framework import status,response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from .serializers import BaseUserSerializer,PatientSerializer,DoctorSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from . import permission
from core.utils import Custom_CheckPermisson
import uuid
from django.core.files.storage import default_storage


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class BaseUserAPI(ModelViewSet):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = []


    @action(methods = ['patch'], detail = False, url_path='change-password')
    def change_password(self,request):       
        request.data._mutable=True 
        new_password=request.data.get('new_password')
        instance=request.user
        
        try:
            validate_password(new_password)
        except Exception as e:
            return JsonResponse({
                'message':'Password dont guarante for confidential','password':list(e),'flag':'false','status':'400'},
            )
     
        instance.password=new_password
        instance.save()
        return JsonResponse({
                'message':'Sucessfully',
                **get_tokens_for_user(request.user),
                'flag':'true',
                'status':'200',
                },
                status=status.HTTP_200_OK
        )
        
        
    
    @action(methods = ['patch'], detail = False, url_path='reset-password')
    def reset_password(self,request):
       
        email=request.data.get('email',None)
        conditions=request.session.get('exchangeable_password',None)
        if conditions is not None and email is not None:
            if email != conditions['email']:
                return JsonResponse({'message':'Forbiden, Confirm otp before reseting password','flag':'false','status':'403'})
            
            instance=BaseUser.objects.get(email=email)
            data=request.POST
            new_password=data.get('new_password')
            try:
                validate_password(new_password)
            except Exception as e:
                return JsonResponse({
                    'message':'Password dont guarante for confidential','password':list(e),'flag':'false','status':'400'}
                )
                
            instance.password=new_password
            instance.save()

            request.session.__delitem__('exchangeable_password')# del flag change pass
            
            return JsonResponse({'message':'successfully','flag':'true','status':'200'})
        else:
            return JsonResponse({'message':'Forbiden, Confirm otp before reseting password','flag':'false','status':'403'})
        
    @action(methods = ['post'], detail = False, url_path='check-password')
    def check_password(self,request):
        old_password=request.data.get('old_password')
        if request.user.check_password(old_password):
            return JsonResponse({'message':'Old password matched','flag':'true','status':'200'})
        else:
            return JsonResponse({'message':'Old password did not match','flag':'false','status':'400'})
    
    
def is_valid(serializer,status):
    try:
        serializer.is_valid(raise_exception=True)
    except Exception as e:
        dict_error=e.__dict__['detail']
        dict_error['flag']='false'
        dict_error['status']=status

        return False, dict_error
    return True,{}

def split_name(full_name):
    arr=full_name.split(" ")
    surname=arr[0:-1]
    firstname=arr[-1]

    if len(surname)==0:
        surname=""
    else:
        surname=" ".join(surname)

    return surname,firstname
    
   
class PatientAPI(Custom_CheckPermisson,ModelViewSet):
    queryset = Patient.objects.all()    
    serializer_class = PatientSerializer
    permission_classes = [permission.CreateAction | (IsAuthenticated & (permission.IsOwner|permission.IsAdmin))]
    

    def get_permissions(self):
        setattr(self.request,'action',self.action)

        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):        
        base_user_data=request.data['base_user']
      
        patient_id=Patient.generate_patient_id()
        request.data['patient_id']=patient_id
        surname,firstname=split_name(base_user_data.pop('full_name'))

        base_user_data['surname']=surname
        base_user_data['firstname']=firstname
        
        serializer = self.get_serializer(data=request.data)
        
        check,dict_error=is_valid(serializer,'400')
        if not check:
            return JsonResponse({**dict_error,**dict_error})
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data=serializer.data
        extra_data={'flag':'true','status':'201'}
        
        
        return response.Response({**data,**extra_data}, status=status.HTTP_201_CREATED, headers=headers)

      
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        base_user_data=request.data['base_user']

        instance = self.get_object()
        surname,firstname=split_name(base_user_data.pop('full_name'))

        base_user_data['surname']=surname
        base_user_data['firstname']=firstname

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        check,dict_error=is_valid(serializer,'400')
        if not check:
            return JsonResponse(dict_error)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        data=serializer.data
        data['flag']='true'
        data['staus']='201'
        return response.Response(data)
    

def find_field(se):
        current_object_fields=se.fields
        nested_object_fields=dict(current_object_fields.pop('base_user').fields).keys() #get keys
        current_object_fields=current_object_fields.keys() #get keys
        return list(nested_object_fields)

def match_data(request,serializer,*extra_field_base_user):
    nested_object_fields=find_field(DoctorSerializer())
    temp={'base_user':{}}
    for key,value in request.data.items():
        if  key in nested_object_fields or key in extra_field_base_user :
            temp['base_user'].update({key:value})
        else:
            temp.update({key:value})  
    return temp
    
    

class DoctorAPI(ModelViewSet):
    queryset = Doctor.objects.all()    
    serializer_class = DoctorSerializer
    permission_classes=[permission.CreateAction |(permission.IsOwner)]

    def get_permissions(self):

        setattr(self.request,'action',self.action)
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        request.data._mutable=True
        data=match_data(request,self.serializer_class(),'full_name')
        
        doctor_id=Doctor.generate_doctor_id()
        data['doctor_id']=doctor_id
      
        surname,firstname=split_name(data['base_user'].pop('full_name'))
        print(data)
        data['base_user']['surname']=surname
        data['base_user']['firstname']=firstname
        
        # store image firebase
        notarized_image=data.pop('notarized_image')
        name=str(uuid.uuid4())+"."+notarized_image.name.split('.')[-1]
        data['notarized_image']=name
        
        serializer = self.get_serializer(data=data)
        
        check,dict_error=is_valid(serializer,'400')
        if not check:
            return JsonResponse({**dict_error,**dict_error})
        
        default_storage.save(name, notarized_image)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data=serializer.data
        extra_data={'flag':'true','status':'201'}
        
        
        return response.Response({**data,**extra_data}, status=status.HTTP_201_CREATED, headers=headers)
              

    