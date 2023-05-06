from rest_framework.permissions import BasePermission
from apps.Booking.models import ConnectDoctor
from apps.User.references import REVERSE_USER_TYPE,RELATED_USER

class IsPatient(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type==REVERSE_USER_TYPE['Patient']:
            return True
        return False
    

class IsDoctor(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type==REVERSE_USER_TYPE['Doctor']:
            return True
        return False
          
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type==REVERSE_USER_TYPE['Admin']:
            return True
        return False
          
class PermitedAction(BasePermission):
    
    def has_permission(self, request, view):
        if request.action in ['create']:
            return True
        return False

# class ApproveAction(BasePermission):
    
#     def has_permission(self, request, view):
#         if request.action=="active" or request.action=="inactive":
#             if request.user:
#             return True
#         return False
    
class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user=request.user
        return getattr(user,RELATED_USER[user.user_type])==obj
        
class InConversation(BasePermission):

    def has_object_permission(self, request, view, obj):
        if REVERSE_USER_TYPE['Doctor']==request.user.user_type:
            doctor=request.user.user_doctor
            if ConnectDoctor.objects.filter(
                doctor=doctor,
                patient=obj
            ).exists():
                return True
        return False
