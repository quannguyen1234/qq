from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views
router=SimpleRouter(trailing_slash=False)
router.register('accounts',views.BaseUserAPI)
router.register('patients',views.PatientAPI)
router.register('doctors',views.DoctorAPI)


urlpatterns=[
    path('',include(router.urls)),
]