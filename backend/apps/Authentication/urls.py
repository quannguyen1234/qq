from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns=[
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/otp/send_otp',views.otp_api),
    path('api/otp/verify_otp',views.verify_otp_api),  
    path('api/check_existed_phone',views.check_existed_phone)
]