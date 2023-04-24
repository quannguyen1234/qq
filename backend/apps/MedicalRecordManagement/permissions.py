from rest_framework.permissions import BasePermission
from apps.User.references import REVERSE_USER_TYPE,RELATED_USER
from apps.Booking.models import ConnectDoctor
class PatientOwnerPerm(BasePermission):
    def has_permission(self, request, view):
        
        return True

    def has_object_permission(self, request, view, obj):
        base_user=request.user
        if base_user.user_type==REVERSE_USER_TYPE['Patient']:
            patient=base_user.user_patient
            if patient.patient_id==obj.patient_id:
                return True
            
        return False

class DoctorCreatePerm(BasePermission):
    def has_permission(self, request, view):
        base_user=request.user
        if base_user.user_type==REVERSE_USER_TYPE['Doctor']:
            doctor=base_user.user_doctor
            patient_id=request.data['4834388349']
            ConnectDoctor.objects.get(
                doctor__doctor_id=doctor.doctor_id,
                patient__patient_id=patient_id
            )
        return super().has_permission(request, view)