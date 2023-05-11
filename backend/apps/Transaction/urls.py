from django.urls import path,include
from .import views
from rest_framework import routers

router=routers.DefaultRouter(trailing_slash=False)
router.register('diagnostic-bills',views.DiagnosticBillAPI)

urlpatterns=[

]
urlpatterns+=router.urls