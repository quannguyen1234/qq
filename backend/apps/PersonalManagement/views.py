from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import HospitalDepartment
from core.utils import Custom_CheckPermisson
from .serializer import HospitalDepartmentSerializer
from django.db.transaction import atomic
class HospitalDepartmentAPI(Custom_CheckPermisson,ModelViewSet):
    serializer_class=HospitalDepartmentSerializer
    # permission_classes=[IsAuthenticated]
    permission_classes=[]
    queryset=HospitalDepartment.objects.all()
    

    @atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data=serializer.data
        data.update({'flag':True,'status':201})
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            data=serializer.data
   
            return Response({'data':data,'status':200,'flag':True})
        except:
            return Response({'data':data,'status':409,'flag':False})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'status':200,'flag':True})