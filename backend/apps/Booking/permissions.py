from rest_framework.permissions import BasePermission

class ListAppointmentPermission:
    doctor_per=['receive_order']

class DoctorAppointmentsPer(BasePermission):
    def has_permission(self, request, view):
      
        if request.user.user_doctor is not None and request.action in ListAppointmentPermission.doctor_per :
            return True
        return False
    
        