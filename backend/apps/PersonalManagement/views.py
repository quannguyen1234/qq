from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import HospitalDepartment
from core.utils import Custom_CheckPermisson
from .serializer import HospitalDepartmentSerializer
class HospitalDepartmentAPI(Custom_CheckPermisson,ModelViewSet):
    serializer_class=HospitalDepartmentSerializer
    permission_classes=[IsAuthenticated]
    queryset=HospitalDepartment.objects.all()
   
    