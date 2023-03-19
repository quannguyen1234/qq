import math, random
from apps.User.models import BaseUser
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json 
import datetime
from datetime import timedelta
from apps.Notification import functions
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from apps.User.references import RELATED_USER
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.token_blacklist.models import  OutstandingToken

@csrf_exempt
def expried_token(request):
    refresh_token=request.POST.get('refresh',None)
    if refresh_token is not None:
        try:
            refresh_token=RefreshToken(token=refresh_token)
            refresh_token.check_blacklist()
            refresh_token.blacklist()
        except:
            return JsonResponse({'message':'refresh token expried or not exist','flag':False},status=status.HTTP_400_BAD_REQUEST)
    
    return JsonResponse({'message':'Sucessfully','flag':True})

@require_http_methods(['GET'])
@csrf_exempt
def check_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    try:
        token=AccessToken(token=token,verify=True)
    except Exception as e:
        return JsonResponse({'message':str(e),'flag':False},status=status.HTTP_403_FORBIDDEN)
    
    base_user=BaseUser.objects.get(id=token.payload['user_id'])
    user=getattr(base_user,RELATED_USER[base_user.user_type])
    
    user_infor={
        'id':user.get_id(),
        'phone_number':base_user.phone_number,
        'gender':base_user.gender,
        'full_name':f"{base_user.surname} {base_user.firstname}",
        'role':base_user.user_type,
        'email':base_user.email
    }
    
    return JsonResponse(
        {
            'user':user_infor,
            'flag':True
        }
    )

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

def send_otp(receiver):
    OTP=generate_otp()
    ###
        #"code here"
    ###
    body=f"""
        Hello, The message from doctor famirly , here is  your OTP : {OTP} 
        """
    functions.send_email(receiver,"Reset Password",body)
    return OTP

@require_http_methods(['POST'])
@csrf_exempt
def check_existed_email(request):
    
    email=request.POST.get('email')
    check=BaseUser.objects.filter(email=email).exists()
    if check:
        return JsonResponse({'message':'Existed','flag':True})
    else:
        return JsonResponse({'message':'Has not existed the email','flag':False})

@require_http_methods(['POST'])
@csrf_exempt
def otp_api(request):
    email=request.POST.get('email',None)
    check_mail=False
    if BaseUser.objects.filter(email=email).exists():
        check_mail=True

    if  email is not None  and check_mail:
        OTP=send_otp(email)
        
        now=datetime.datetime.now()
        request.session['otp']={}
        request.session.set_expiry(300)
        dict_otp=request.session.get('otp')
        dict_otp['code_otp']=OTP
        dict_otp['email']=email
        dict_otp['timeout_otp']={
            'time':json.dumps(now+timedelta(minutes=3),default=serialize_datetime),
        }
        return JsonResponse({'message':'Successfully','flag':True})
    else:
        return JsonResponse({'message':'Not exist email','flag':False},status=status.HTTP_400_BAD_REQUEST)


@require_http_methods(['POST'])
@csrf_exempt
def verify_otp_api(request):
    dict_otp=request.session.get('otp')
    otp1=request.POST['otp']
    otp2=dict_otp['code_otp']
    email=dict_otp['email']
    time=request.session['otp']['timeout_otp']['time']
    # print(datetime.datetime.strptime(time,'%Y-%d-%M%H:%M:%S'))
    
    if otp1 == otp2:
        request.session['exchangeable_password']={
            'email':email,
            'check':True
        }

        return JsonResponse({'message':'Successfully','flag':True})
    else:
        return JsonResponse({'message':'OTP has not right','flag':False},status=status.HTTP_400_BAD_REQUEST)
    
    



    
