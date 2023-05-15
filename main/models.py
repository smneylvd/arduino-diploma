from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.serializers import serialize
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)

    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.nickname

    def serialize(self):
        serialized_data = serialize('json', [self])
        return serialized_data


class Device(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def serialize(self):
        serialized_data = serialize('json', [self])
        return serialized_data


class AccessList(models.Model):
    access_type = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255, default="")

    def serialize(self):
        serialized_data = serialize('json', [self])
        return serialized_data


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    action = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        serialized_data = serialize('json', [self])
        return serialized_data
