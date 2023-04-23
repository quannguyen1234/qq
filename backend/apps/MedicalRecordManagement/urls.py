from django.urls import path,include
from .import views
from rest_framework import routers

router=routers.DefaultRouter(trailing_slash=False)
router.register('medical-records',views.MedicalRecordAPI)

urlpatterns=[

]
urlpatterns+=router.urls