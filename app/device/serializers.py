from django.contrib.auth import (
    get_user_model,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import Device


class DeviceSerializer(serializers.ModelSerializer):
    """Serializer for device object"""
    class Meta:
        model = Device
        fields = ['id', 'device_uuid', 'device_name', 'device_type']
        read_only_fields = ['id']

    def create(self, validated_data):
        """create a new device model"""
        device = Device.objects.create(**validated_data)
        device.users.add(self.context['request'].user)
        return device

    def update(self, instance, validated_data):
        """update existing device model"""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance