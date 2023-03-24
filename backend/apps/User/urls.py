from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views

router=SimpleRouter(trailing_slash=False)
router.register('patients',views.PatientAPI)
router.register('doctors',views.DoctorAPI)

base_user_router=SimpleRouter(trailing_slash=False)
base_user_router.register('',views.BaseUserAPI)

urlpatterns=[
    path('',include(router.urls)),
]

urlpatterns+=base_user_router.urls