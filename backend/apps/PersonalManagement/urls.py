from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views

router=SimpleRouter(trailing_slash=False)
router.register('hospital-departments',views.HospitalDepartmentAPI)



urlpatterns=[
    path('',include(router.urls)),
]
