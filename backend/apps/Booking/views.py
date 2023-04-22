from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.User.models import Doctor
from .serializers import DoctorAppointmentsSerializer
from rest_framework.decorators import action
from apps.User.permission import IsDoctor
from apps.PersonalManagement.models import Address 
from core.references import AddressEnum
from django.db.transaction import atomic
from django.http import JsonResponse
from .permissions import DoctorAppointmentsPer
# from .models import Appointment

class DoctorAppointmentsAPI(GenericViewSet):
    # permission_classes = [IsAuthenticated & (IsDoctor&DoctorAppointmentsPer)]
    permission_classes=[]
    queryset=Doctor.objects.all()
    serializer_class=DoctorAppointmentsSerializer   
    
    def get_permissions(self):
        
        setattr(self.request,'action',self.action)
        return super().get_permissions()
    
    @action(methods=['get'],detail=False,url_path='get-doctors')
    def get_doctors(self,request):
        data=request.data
        address=data.pop('address')
        department=data.pop('de_id')
        district=address.get('district')
        city=address.get('city')
     
        addresses=Address.objects.filter(
            district__iregex=f"{district}",
            city__iregex=f"{city}"
        )
        
        #filter doctors is free
        doctors=Doctor.objects.filter(
            is_receive=True,
            departments__de_id=department,
            base_user__address__in=addresses
        )
        if len(doctors)==0:
            return JsonResponse({
                'flag':False,
                'status':200,
                'message':'No doctors'
            })
        doctors_data=DoctorAppointmentsSerializer(doctors,many=True).data
       
        data=[]
        for doctor_data in doctors_data:
            data.append(dict(doctor_data))
    
        # return JsonResponse({'doctors':data})
        return JsonResponse({'doctors':data,'flag':True,'status':200})

    @atomic
    @action(methods=['POST'],detail=False,url_path='receive-order')
    def receive_order(self,request,*args, **kwargs):
        try:
            doctor=request.user.user_doctor
            status=request.data.get('status')
            doctor.is_receive=status
            doctor.save()
            address=request.data.get('address')
            Address.objects.filter(base_user__email=request.user.email,address_type=AddressEnum.CurrentAddress.value).delete()
            if status:
                Address.objects.create(**address,base_user=request.user,address_type=AddressEnum.CurrentAddress.value)
            return JsonResponse({
                'status':200,
                'flag':True
            })
        except:
            return JsonResponse({
                'status':409,
                'flag':False
            })
        
def receive_order(base_user,data):
    address=data.get('address')
    Address.objects.filter(base_user__email=base_user.email,address_type=AddressEnum.CurrentAddress.value).delete()
    Address.objects.create(**address,base_user=base_user,address_type=AddressEnum.CurrentAddress.value)