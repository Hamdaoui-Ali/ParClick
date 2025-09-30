from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class ClientManager(BaseUserManager):
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        client = self.model(email=email, full_name=full_name)
        client.set_password(password)
        client.save(using=self._db)
        return client

    def create_superuser(self, email, full_name, password):
        client = self.create_user(email=email, full_name=full_name, password=password)
        client.is_staff = True
        client.is_superuser = True
        client.save(using=self._db)
        return client

class Client(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='client_groups',
        blank=True,
        help_text='The groups this client belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='client_permissions',
        blank=True,
        help_text='Specific permissions for this client.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = ClientManager()

    def __str__(self):
        return self.full_name

# models.py

import random
import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models
from django.conf import settings
from datetime import timedelta

# --------------------------
# PARKING PLACE
# --------------------------

class ParkingPlace(models.Model):
    number = models.CharField(max_length=5, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Place {self.number} - {'Available' if self.is_available else 'Occupied'}"


# --------------------------
# RESERVATION
# --------------------------
from django.utils.timezone import make_aware, is_naive
class Reservation(models.Model):
    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle')
    ]

    PAYMENT_TYPES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card')
    ]

    ticket_id = models.PositiveIntegerField(unique=True, blank=True, null=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey(ParkingPlace, on_delete=models.CASCADE)
    vehicule_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField(null=True, blank=True)  # in hours
    price = models.FloatField(default=0)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)


    
    def save(self, *args, **kwargs):
        
        if self.start_time and is_naive(self.start_time):
            self.start_time = make_aware(self.start_time)
        if self.end_time and is_naive(self.end_time):
            self.end_time = make_aware(self.end_time)
        
        # 1. Ticket ID
        if not self.ticket_id:
            while True:
                new_id = random.randint(1000, 9999)
                if not Reservation.objects.filter(ticket_id=new_id).exists():
                    self.ticket_id = new_id
                    break

        # 2. Duration & Price
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration = round(delta.total_seconds() / 3600, 2)

            if self.vehicule_type == 'car':
                self.price = round(self.duration * 5, 2)
            elif self.vehicule_type == 'motorcycle':
                self.price = round(self.duration * 2, 2)

        # 3. QR Code
        qr_data = f"Reservation: {self.ticket_id} | Client: {self.client.email} | Place: {self.place.number}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        file_name = f'{self.ticket_id}_qr.png'
        self.qr_code.save(file_name, File(buffer), save=False)
        buffer.close()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation {self.ticket_id} - {self.place.number}"
    
# --------------------------
# HISTORY
# --------------------------
class History(models.Model):
    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('motorcycle', 'Motorcycle')
    ]

    PAYMENT_TYPES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card')
    ]

    ticket_id = models.PositiveIntegerField(unique=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey(ParkingPlace, on_delete=models.SET_NULL, null=True)
    vehicule_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField()
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    price = models.FloatField()
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return f"History {self.ticket_id} - {self.place.number if self.place else 'N/A'}"

