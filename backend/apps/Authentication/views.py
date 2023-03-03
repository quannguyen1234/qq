import math, random
from apps.User.models import BaseUser
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json 
import datetime
from datetime import timedelta

def serialize_datetime(obj): 

    if isinstance(obj, datetime.datetime): 

        return obj.isoformat() 

    raise TypeError("Type not serializable") 
def generate_otp():
    digits = "0123456789"
    OTP = ""

   # length of password can be changed
   # by changing value in range

    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def send_otp():
    OTP=generate_otp()
    ###
        #"code here"
    ###
    return OTP

@require_http_methods(['POST'])
@csrf_exempt
def check_existed_phone(request):
    print(request.body)
    phone_number=request.POST.get('phone_number')
    check=BaseUser.objects.filter(phone_number=phone_number).exists()
    if check:
        return JsonResponse({'message':'oke'})
    else:
        return JsonResponse({'message':'Has not existed the phone number'},status=status.HTTP_400_BAD_REQUEST)

@require_http_methods(['POST'])
@csrf_exempt
def otp_api(request):
    phone_number=request.POST.get('phone_number')
    if  phone_number is not None and BaseUser.objects.filter(phone_number=phone_number).exists():
        OTP=send_otp()
        print(OTP)
        now=datetime.datetime.now()
        request.session['otp']={}
        dict_otp=request.session.get('otp')
        dict_otp['code_otp']=OTP
        dict_otp['phone_number']=phone_number
        dict_otp['timeout_otp']={
            'time':json.dumps(now+timedelta(minutes=3),default=serialize_datetime),
        }
        return JsonResponse({'message':'oke'})
    else:
        return JsonResponse({'message':'Not exist phone number'},status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(['POST'])
@csrf_exempt
def verify_otp_api(request):
    dict_otp=request.session.get('otp')
    otp1=request.POST['otp']
    otp2=dict_otp['code_otp']
    phone_number=dict_otp['phone_number']
    time=request.session['otp']['timeout_otp']['time']
    # print(datetime.datetime.strptime(time,'%Y-%d-%M%H:%M:%S'))
    print(time)
    if otp1 == otp2:
        # request.session.de
        request.session['exchangeable_password']={
            'phone_number':phone_number,
            'check':True
        }
        return JsonResponse({'message':'oke'})
    else:
        return JsonResponse({'message':'OTP has not right'},status=status.HTTP_400_BAD_REQUEST)
    
    



    
