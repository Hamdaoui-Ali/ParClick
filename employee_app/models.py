import random
import qrcode
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Employees must have an email address")
        email = self.normalize_email(email)
        employee = self.model(email=email, **extra_fields)
        employee.set_password(password)
        employee.save(using=self._db)
        return employee

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Employee(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    employee_cin = models.CharField(max_length=8, unique=True)
    employee_phone = models.CharField(max_length=15, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='employee_groups',
        blank=True,
        help_text='The groups this employee belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='employee_permissions',
        blank=True,
        help_text='Specific permissions for this employee.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employee_id', 'full_name', 'employee_cin', 'employee_phone']

    objects = EmployeeManager()

    def __str__(self):
        return self.full_name

