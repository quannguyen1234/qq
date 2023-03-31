from .models import Patient,Doctor,BaseUser
from apps.PersonalManagement.models import DoctorDepartment,HospitalDepartment
from rest_framework import status,response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, JSONParser,FormParser
from rest_framework.decorators import action
from django.http import JsonResponse
from django.core.cache import cache
from .serializers import PatientSerializer,DoctorSerializer
from . import permission
from core.references import ImageEnum
from core.utils import( Custom_CheckPermisson,
 split_name,is_valid,process_image,save_file,set_name_file,upload_image
)
from apps.User.serializers import BaseUserSerializer
from django.contrib.auth.password_validation import validate_password
from django.db.transaction import atomic
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
        
        check,dict_error=is_valid(serializer,400)
        if not check:
            return JsonResponse({**dict_error,**dict_error})
            
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data=serializer.data
        extra_data={'flag':True,'status':201}
        
        
        return response.Response({**data,**extra_data}, status=status.HTTP_201_CREATED, headers=headers)

      
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        base_user_data=request.data['base_user']

        instance = self.get_object()
        surname,firstname=split_name(base_user_data.pop('full_name'))

        base_user_data['surname']=surname
        base_user_data['firstname']=firstname

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        check,dict_error=is_valid(serializer,400)
        if not check:
            return JsonResponse(dict_error)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        data=serializer.data
        data['flag']=True
        data['staus']=201
        return response.Response(data)
    

class DoctorAPI(Custom_CheckPermisson,ModelViewSet):
    queryset = Doctor.objects.all()    
    serializer_class = DoctorSerializer
    permission_classes=[]
    # permission_classes=[permission.CreateAction |(IsAuthenticated & (permission.IsAdmin |permission.IsOwner))]
    
    def get_permissions(self):

        setattr(self.request,'action',self.action)
        return super().get_permissions()
    
    def perform_create(self, serializer):
        instance=serializer.save()
        return instance
    
    @atomic
    def create(self, request, *args, **kwargs):
        
        data=request.data

        doctor_id=Doctor.generate_doctor_id()
        data['doctor_id']=doctor_id
      
        surname,firstname=split_name(data['base_user'].pop('full_name'))

        data['base_user']['surname']=surname
        data['base_user']['firstname']=firstname
        
        if data.__contains__('departments'):
            departments=data.pop('departments') # remove from serializer
        else:
            departments=[]

        serializer = self.get_serializer(data=data)
        
        check,dict_error=is_valid(serializer,'400')
        
        if not check:
            return JsonResponse({**dict_error,**dict_error})
        
        
        intance=self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        

        
        for department in departments:
            if department['de_id']=='0':
                de=HospitalDepartment.objects.create(
                    name=department['name']
                )
                intance.departments.add(de)
            else:
                try:
                    de=HospitalDepartment.objects.get(de_id=department['de_id'])
                    intance.departments.add(de)
                except:
                    pass
        
        data=DoctorSerializer(intance).data
        extra_data={'flag':True,'status':201}
        
        
        return response.Response({**data,**extra_data}, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'],detail=False,url_path='upload-notarized-doctor-images')
    def upload_notarized_image(self,request):
        try:
            print(request.data)
            list_notarized_image,list_name=set_name_file(request.data,'images')
            urls=[]
        
            for index,image in enumerate(list_notarized_image):
                name=list_name[index]
                save_file(name,image)
                url=upload_image(name,'images/notarized_image',ImageEnum.DoctorNotarizedImage.value)
                urls.append(url)
            return JsonResponse({'status':200,'flag':True,'urls':urls})
        except:
            return JsonResponse({'status':409,'flag':False})

    @action(methods=['post'],detail=True,url_path='active')
    def approve_doctor(self,request,pk=None):
        try:
            instance=self.get_object()
            instance.base_user.active_user()
            return JsonResponse({'message':'Active Successfully','status':200,'flag':True})
        except:
            return JsonResponse({'message':'Active Fail','status':409,'flag':False})
        
    @action(methods=['post'],detail=True,url_path='inactive')
    def inapprove_doctor(self,request,pk=None):
        instance=self.get_object()
        instance.base_user.inactive_user()
        return JsonResponse({'message':'Inactive Successfully','status':201,'flag':True})
    



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
                'message':'Password dont guarante for confidential','password':list(e),'flag':False,'status':400},
            )
     
        instance.set_password(new_password)
        instance.save()
        return JsonResponse({
                'message':'Sucessfully',
                **get_tokens_for_user(request.user),
                'flag':True,
                'status':200,
                },
                status=status.HTTP_200_OK
        )
        
        
    
    @action(methods = ['patch'], detail = False, url_path='reset-password')
    def reset_password(self,request):
       
        email=request.data.get('email',None)
        conditions=cache.get(f'{email}_exchangeable_password',False)
        
        if conditions != False and email is not None:

            instance=BaseUser.objects.get(email=email)
            data=request.data
            new_password=data.get('new_password')
            try:
                validate_password(new_password)
            except Exception as e:
                return JsonResponse({
                    'message':'Password dont guarante for confidential','password':list(e),'flag':False,'status':400}
                )
            
            instance.set_password(new_password)
            instance.save()
            
            return JsonResponse({'message':'successfully','flag':True,'status':200})
        else:
            return JsonResponse({'message':'Forbiden, Confirm otp before reseting password','flag':False,'status':403})
        
    @action(methods = ['post'], detail = False, url_path='check-password')
    def check_password(self,request):
        old_password=request.data.get('old_password')
        if request.user.check_password(old_password):
            return JsonResponse({'message':'Old password matched','flag':True,'status':200})
        else:
            return JsonResponse({'message':'Old password did not match','flag':False,'status':400})
    
    
