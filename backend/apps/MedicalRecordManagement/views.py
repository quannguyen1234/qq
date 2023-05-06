from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework import status,response
from .import serializers
from django.db.transaction import atomic
from core.utils import is_valid
from django.http import JsonResponse
from rest_framework.decorators import action
from apps.User.models import Patient
from rest_framework.exceptions import ValidationError
import datetime
# from rest_framework.permissions import IsAuthenticated
# class PrescriptionAPI(ModelViewSet):
    # queryset=Pre

class MedicalRecordAPI(ModelViewSet):
    queryset=MedicalRecord.objects.all()
    permission_classes=[]
    serializer_class=serializers.MedicalRecordSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        data['flag']=True
        data['status']=200
        return JsonResponse(data)

    @atomic
    def create(self, request, *args, **kwargs):
        doctor=request.user.user_doctor
        data=request.data
        data['date']=datetime.datetime.now()
        data['doctor']=doctor.doctor_id
        
        serializer = self.get_serializer(data=data)

        check,dict_error=is_valid(serializer,400)
        if not check:
            return JsonResponse({**dict_error,**dict_error})
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data={
            'data':data,
            'flag':True,
            'status':200
        }
        return response.Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    @atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        check,dict_error=is_valid(serializer,400)
        if not check:
            return JsonResponse({**dict_error,**dict_error})
        
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        data=serializer.data
        data['flag']=True
        data['status']=200
        return response.Response(data)


    def get_patient(self,patient_id):
        try:
            patient=Patient.objects.get(patient_id=patient_id)
        except:
            return None,{'flag':False,'status':400,'message':'patient id is not correct'}
        return patient,{}
        

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data={
            'data':serializer.data,
            'flag':True,
            'status':200
        }
        return response.Response(data)
    
    @action(methods=['GET'],detail=False,url_path='patient/(?P<patient_id>.+)/$')
    def get_patients_records(self,request,patient_id=None):
        
        patient,message=self.get_patient(patient_id)
        if patient is  None:
            return JsonResponse(message)
        records=patient.records.all()
        data=serializers.MedicalRecordSerializer(records,many=True).data
        for index,record in enumerate(records):
            current_base_user=record.doctor.base_user
            current_record=data[index]
            current_record['doctor_name']=current_base_user.get_full_name
            current_record['current_job']=record.doctor.current_job
            current_record['departments']=list(record.doctor.departments.all().values_list('name',flat=True))
        
            
        return JsonResponse({'data':data,'flag':True,'status':200})

    
    @action(methods=['GET'],detail=False,url_path='doctor/(?P<doctor_id>.+)/$')
    def get_record_by_doctor(self,request,doctor_id):
        records=MedicalRecord.objects.all()
        data=[]
        current_year=datetime.datetime.now().year
        for record in records:
            record_data={}
            base_user=record.patient.base_user
            record_data['patient_name']=base_user.get_full_name
            try:
                age=current_year-base_user.birth_day.year
            except:
                age=None
            record_data['age']=age 
            try:
                gender=base_user.gender
            except:
                gender=None
            record_data['gender']=gender
            record_data['date']=f"{record.date.month}-{record.date.month}-{record.date.year}"
            data.append(record_data)
        return JsonResponse({'data':data,'flag':True,'status':200})
            

