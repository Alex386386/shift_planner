from django.urls import include, path
from rest_framework import routers

from .views import MonthViewSet, WorkerViewSet

v1_router = routers.DefaultRouter()
v1_router.register('month', MonthViewSet, basename='month')
v1_router.register('worker', WorkerViewSet, basename='worker')

urlpatterns = [
    path('v1/auth/', include('djoser.urls')),
    path('v1/auth/', include('djoser.urls.jwt')),
    path('v1/', include(v1_router.urls)),
]
