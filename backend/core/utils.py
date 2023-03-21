from rest_framework.exceptions import APIException,MethodNotAllowed
from rest_framework import status

class Custom_APIException(APIException):
    status_code = status.HTTP_200_OK
    default_detail = ('You do not have permission to perform this action')
    default_code = 'error'

class Custom_CheckPermisson:
    def check_permissions(self, request):
     
        try:
            super().check_permissions(request)
        except Exception as e:
            
            raise Custom_APIException({
                "message" : "You do not have permission to perform this action.",
                "flag":'false',
                "status":'403'
            })
        
    def check_object_permissions(self,request,obj):
        try:
            super().check_object_permissions(request,obj)
        except Exception as e:
            
            raise Custom_APIException({
                "message" : "You do not have permission to perform this action.",
                "flag":'false',
                "status":'403'
            })
