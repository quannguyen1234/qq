from rest_framework.exceptions import APIException,MethodNotAllowed
from rest_framework import status
class Custom_APIException(APIException):
    status_code = status.HTTP_200_OK
    default_detail = ('You do not have permission to perform this action')
    default_code = 'error'