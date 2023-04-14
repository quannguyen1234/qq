from rest_framework.viewsets import ModelViewSet
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
        return super().create(request, *args, **kwargs)
    