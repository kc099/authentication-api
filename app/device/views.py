from rest_framework import (
    permissions,
    viewsets,
    status)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from device import serializers
from core.models import Device


class DeviceViewSet(viewsets.ModelViewSet):
    """Get/Add/Delete device model"""
    serializer_class = serializers.DeviceSerializer
    query_set = Device.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch',]

    def get_queryset(self):
        """Retrieve devices of authenticated user"""
        return self.query_set.filter(
            users__email=self.request.user.email
        ).order_by('-id').distinct()

