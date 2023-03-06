from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views
router=SimpleRouter(trailing_slash=False)
router.register('base-users',views.BaseUserAPI)
router.register('patients',views.PatientAPI)
from django.http import JsonResponse

urlpatterns=[
    path('',include(router.urls)),
]