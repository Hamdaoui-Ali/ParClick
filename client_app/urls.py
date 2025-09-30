from django.urls import path

from client_app import forms
from client_app.forms import book_reservation, download_ticket
from . import views
from .views import login_register_view

urlpatterns = [
    path('login/', login_register_view, name='client_login'),
    path('logout/', views.client_logout, name='client_logout'),
    path('home/', views.home, name='home'),
    path('reserve/', book_reservation, name='book_reservation'),
    path('success/', views.reservation_success, name='reservation_success'),
    path('reservation/download/', forms.download_ticket, name='download_ticket'),
    path('reservations/', views.my_reservations, name='my_reservations'),
    path('reservations/cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('about/', views.about_page, name='about_page'),
    path('history/', views.client_history_view, name='client_history'),
]