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
 split_name,is_valid,save_file,set_name_file,upload_image
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
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            
            return response.Response({'data':serializer.data,'status':200,'flag':True})
        except:
            return response.Response({'data':serializer.data,'status':409,'flag':False}) 
        
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
    
    def perform_update(self, serializer):
        instance=serializer.save()
        return instance
    
    @action(methods=['GET'],detail=False,url_path='get-doctor')
    def get_doctor_approved(self,request):
        
        approved=request.query_params['approved']
        
        if approved=='0':
            doctors=self.serializer_class(Doctor.objects.filter(base_user__is_active=True),many=True)
            print(doctors)
        else:
            doctors=self.serializer_class(Doctor.objects.filter(base_user__is_active=False),many=True)
        
        return JsonResponse({'data':doctors.data,'status':200,'flag':True})
       

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
        
        check,dict_error=is_valid(serializer,400)
        
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

    @atomic
    def update(self, request, *args, **kwargs):
        
        if request.data['base_user'].__contains__('full_name'):
       
            surname,firstname=split_name(request.data['base_user'].pop('full_name'))
            request.data['base_user']['surname']=surname
            request.data['base_user']['firstname']=firstname
     
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        check,dict_error=is_valid(serializer,400)
        if not check:
            return JsonResponse({**dict_error,**dict_error})
        instance=self.perform_update(serializer)



        if request.data.__contains__('departments'):
            
            DoctorDepartment.objects.filter(doctor=instance).delete()
            departments=request.data.pop('departments')
            for de  in departments:
                if de['de_id']=='0':
                    de=HospitalDepartment.objects.create(
                        name=de['name']
                    )
                else:
                    de=HospitalDepartment.objects.get(de_id=de['de_id'])
                instance.departments.add(de)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        data=serializer.data
        data.update({'flag':True,'status':200})
        return response.Response(data)

    @atomic
    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        instance.base_user.delete()
        return JsonResponse({'d':'d'})
        # return super().destroy(request, *args, **kwargs)
    
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
    
    
