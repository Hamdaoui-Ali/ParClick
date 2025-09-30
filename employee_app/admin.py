from django.contrib import admin
from client_app.models import ParkingPlace, Reservation, Client, History
from employee_app.models import Employee

# Register your models here.
admin.site.register(ParkingPlace)
admin.site.register(Reservation)
admin.site.register(Employee)
admin.site.register(History)
admin.site.register(Client)  # Assuming Client is defined in client_app.models
