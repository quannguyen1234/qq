from django.urls import path,include
from rest_framework.routers import SimpleRouter
from . import views
router=SimpleRouter(trailing_slash=False)
router.register('base_users',views.BaseUserAPI)
from django.http import JsonResponse

urlpatterns=[
    path('',include(router.urls)),
]