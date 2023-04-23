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
# from rest_framework.permissions import IsAuthenticated
# class PrescriptionAPI(ModelViewSet):
    # queryset=Pre

class MedicalRecordAPI(ModelViewSet):
    queryset=MedicalRecord.objects.all()
    permission_classes=[]
    serializer_class=serializers.MedicalRecordSerializer
    
    # @atomic
    # def create(self, request, *args, **kwargs):
        
    #     serializer = self.get_serializer(data=request.data)
    #     # serializer.is_valid(raise_exception=True)
    #     check,dict_error=is_valid(serializer,400)

    #     if not check:
    #         return JsonResponse({**dict_error,**dict_error})
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     data={
    #         'data':data,
    #         'flag':True,
    #         'status':200
    #     }
    #     return response.Response(data, status=status.HTTP_201_CREATED, headers=headers)
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
    def get_patients_record(self,request,patient_id=None):
        
        patient,message=self.get_patient(patient_id)
        if patient is  None:
            return JsonResponse(message)
        records=patient.records.all()
        data=serializers.MedicalRecordSerializer(records,many=True).data
        return JsonResponse({'data':data})
    
    
