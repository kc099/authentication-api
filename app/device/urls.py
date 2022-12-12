"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from device import views


router = DefaultRouter()
router.register(r'device', views.DeviceViewSet, basename='Device')

app_name = 'device'

urlpatterns = [
    path('', include(router.urls)),
]