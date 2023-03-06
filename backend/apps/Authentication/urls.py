from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns=[
    path('token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('otp/send-otp',views.otp_api),
    path('otp/verify-otp',views.verify_otp_api),  
    path('check-existed-phone',views.check_existed_phone)
]