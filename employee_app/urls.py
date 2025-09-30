from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.employee_login, name='employee_login'),
    path('logout/', views.employee_logout, name='employee_logout'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'), 
    path('parking/', views.parking_view, name='parking'),
    path('reservation/', views.reservation_list, name='reservation_list'),
    path('reservation/edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    path('reservation/delete/<int:pk>/', views.delete_reservation, name='delete_reservation'),
    path('reservation/validate/<int:reservation_id>/', views.validate_reservation, name='validate_reservation'),
    path('reservations/validate_all/', views.validate_all_expired_reservations, name='validate_all_expired'),
    path('history/', views.history_view, name='history'),
]
