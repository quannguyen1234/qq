from rest_framework.exceptions import APIException,MethodNotAllowed
from rest_framework import status
import uuid
from django.core.files.storage import default_storage
from core.config_outsystems.cfg_firebase import storage,firebase_admin
import os 
from core.references import ImageEnum
from apps.PersonalManagement.models import Image
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


def is_valid(serializer,status):
    try:
        serializer.is_valid(raise_exception=True)
    except Exception as e:
        print("------cxd---",e)
        dict_error=e.__dict__['detail']
        dict_error['flag']='false'
        dict_error['status']=status
        return False, dict_error
    return True,{}

def split_name(full_name):
    arr=full_name.split(" ")
    surname=arr[0:-1]
    firstname=arr[-1]

    if len(surname)==0:
        surname=""
    else:
        surname=" ".join(surname)

    return surname,firstname





def find_field(se):
        current_object_fields=se.fields
        nested_object_fields=dict(current_object_fields.pop('base_user').fields).keys() #get keys
        current_object_fields=current_object_fields.keys() #get keys
        return list(nested_object_fields)

def handle_file(request,key,file_fields):
    if key in file_fields:
        values=request.data.getlist(key)
        return values
    return None
        
    
def match_data(request,serializer,file_fields,*extra_field_base_user,cls):
    nested_object_fields=find_field(cls())
    temp={'base_user':{}}
    for key,value in request.data.items():

        value_file=handle_file(request,key,file_fields) # check file arr
        if  key in nested_object_fields or key in extra_field_base_user :
            if value_file is not None:
                temp['base_user'].update({key:value_file})
            else:
                temp['base_user'].update({key:value})
            
        else:
            if value_file is not None:
                temp.update({key:value_file})
            else:
                temp.update({key:value})
    return temp
    
def get_file_name(file):
    name=str(uuid.uuid4())+"."+file.name.split('.')[-1]
    return name

def save_file(name,file):
    default_storage.save(name, file)


def set_name_file(data,field_name):
    list_image=data.pop(field_name)
    list_name=[]
    for image in list_image:
        list_name.append(get_file_name(image))
        
    data[field_name]=list_name
    return list_image,list_name




def process_image(instance,name,url):
    
    # check exist image
    list_old_image=Image.objects.filter(
        base_user__user_doctor=instance,
        image_type=ImageEnum.DoctorNotarizedImage.value
    )
    for img in list_old_image:
        try:
            storage.delete("{}/{}".format(url,img.name),firebase_admin['idToken']) 
        except:
            pass
 
    
    storage.child("{}/{}".format(url,name)).put("media/"+name)
    
    if os.path.exists("media/"+name):
        os.remove("media/"+name)

    url=storage.child("images/notarized_image/{}".format(name)).get_url(firebase_admin['idToken'])
    Image.objects.create(
        url=url,
        name=name,
        base_user=instance.base_user,
        image_type=ImageEnum.DoctorNotarizedImage.value
    )
    return url

def upload_image(name,url,image_type):
     
    
    storage.child("{}/{}".format(url,name)).put("media/"+name)
  
    url=storage.child("images/notarized_image/{}".format(name)).get_url(firebase_admin['idToken'])
    Image.objects.create(
        url=url,
        name=name,
        image_type=image_type
    )
    return url
