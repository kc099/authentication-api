"""
Database models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class DeviceManager():
    pass

class Device(models.Model):
    """Device model for user"""
    device_name = models.CharField(max_length=255, blank=True, null=True)
    device_type = models.CharField(max_length=100, blank=True, null=True)
    device_owner = models.EmailField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    device_active = models.BooleanField(default=True)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, name, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have a name')
        user = self.model(email=self.normalize_email(email), name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and return superuser"""
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    # created_at = models.DateTimeField(auto_now_add=True)
    # modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    devices = models.ManyToManyField(Device)

    objects = UserManager()

    USERNAME_FIELD = 'email'


