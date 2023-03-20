from rest_framework.permissions import BasePermission
from apps.User.references import REVERSE_USER_TYPE,RELATED_USER

class IsPatient(BasePermission):

    def has_permission(self, request, view):
        if request.user_type==REVERSE_USER_TYPE['Patient']:
            return True
        return False
          
class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user_type==REVERSE_USER_TYPE['Admin']:
            return True
        return False
          
class CreateAction(BasePermission):
    def has_permission(self, request, view):
        
        if request.action=="create":
            return True
        return False
    
class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
    
        return getattr(request.user,'user_patient')==obj