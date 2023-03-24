from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns=[
    path('login', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout',views.expried_token),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('otp/send-otp',views.otp_api),
    path('otp/verify-otp',views.verify_otp_api),  
    path('check-existed-email',views.check_existed_email),
    path('fetch-user',views.check_token)
]