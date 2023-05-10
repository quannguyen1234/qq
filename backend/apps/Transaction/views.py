from rest_framework.viewsets import ModelViewSet
from .serializers import DiagnosticBillSerializer
from .models import DiagnosticBill,DiagnosticBillDetail


class DiagnosticBillAPI(ModelViewSet):
    serializer_class=DiagnosticBillSerializer
    queryset=DiagnosticBill.objects.all()
    permission_classes=[]
    