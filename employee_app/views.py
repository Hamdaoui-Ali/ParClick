from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

def employee_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('employee_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not an employee.')
    return render(request, 'employee_app/login.html')

def employee_logout(request):
    logout(request)
    return redirect('employee_login')

def staff_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))

from django.contrib.auth.decorators import login_required

# @login_required
def employee_dashboard(request):
    return render(request, 'employee_app/dashboard.html')

from django.shortcuts import render
from client_app.models import ParkingPlace

from client_app.models import ParkingPlace

@staff_required
def parking_view(request):
    places = ParkingPlace.objects.all()
    total = places.count()
    available = places.filter(is_available=True).count()
    occupied = total - available

    return render(request, 'employee_app/parking.html', {
        'places': places,
        'total': total,
        'available_count': available,
        'occupied_count': occupied
    })

from django.db.models import Sum, Count
from django.utils import timezone
from client_app.models import History
from client_app.models import Reservation
from datetime import timezone as dt_timezone


from django.utils import timezone
from django.db.models import Sum
from client_app.models import History, Reservation
from datetime import datetime, timezone as dt_timezone

@staff_required
def employee_dashboard(request):
    today = timezone.now().date()

    # Fix: Use datetime + UTC properly
    year_start = datetime(today.year, 1, 1, tzinfo=dt_timezone.utc)

    today_earnings = History.objects.filter(end_time__date=today).aggregate(Sum('price'))['price__sum'] or 0
    annual_earnings = History.objects.filter(end_time__gte=year_start).aggregate(Sum('price'))['price__sum'] or 0

    current_reservations = Reservation.objects.count()
    total_history = History.objects.count()

    earnings_data = History.objects.extra({'date': "date(end_time)"}).values('date').annotate(total=Sum('price')).order_by('date')
    earnings_dates = [entry['date'] for entry in earnings_data]
    earnings_amounts = [entry['total'] for entry in earnings_data]

    car_count = History.objects.filter(vehicule_type='car').count()
    motorcycle_count = History.objects.filter(vehicule_type='motorcycle').count()

    return render(request, 'employee_app/dashboard.html', {
        'today_earnings': round(today_earnings, 2),
        'annual_earnings': round(annual_earnings, 2),
        'current_reservations': current_reservations,
        'total_history': total_history,
        'earnings_dates': earnings_dates,
        'earnings_amounts': earnings_amounts,
        'car_count': car_count,
        'motorcycle_count': motorcycle_count,
    })

    
from client_app.models import Reservation
from client_app.forms import ReservationForm
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .decorators import staff_required
from client_app.models import Reservation
from django.shortcuts import render

@staff_required
def reservation_list(request):
    reservations = Reservation.objects.all().order_by('-start_time')
    return render(request, 'employee_app/reservation_list.html', {
        'reservations': reservations,
        'now': timezone.now()  # ⏰ Current time sent to the template
    })


@staff_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    old_place = reservation.place

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            updated = form.save(commit=False)
            if old_place != updated.place:
                old_place.is_available = True
                old_place.save()
                updated.place.is_available = False
                updated.place.save()
            updated.save()
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'employee_app/reservation_form.html', {'form': form, 'action': 'Edit'})

@staff_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.place.is_available = True
    reservation.place.save()
    reservation.delete()
    return redirect('reservation_list')

from client_app.models import History, Reservation
from django.utils import timezone
from django.utils.timezone import is_naive, make_aware
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .decorators import staff_required  # assuming you created this
from django.db.models import Q

@staff_required
def validate_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    now = timezone.now()

    # # No need to normalize; just compare directly
    # if reservation.end_time > now:
    #     messages.error(request, "Reservation has not ended yet. Cannot validate.")
    #     return redirect('reservation_list')

    # if not all([reservation.end_time, reservation.duration, reservation.price]):
    #     messages.error(request, "Incomplete reservation data.")
    #     return redirect('reservation_list')

    if request.method == 'POST':
        History.objects.create(
            ticket_id=reservation.ticket_id,
            client=reservation.client,
            place=reservation.place,
            vehicule_type=reservation.vehicule_type,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            duration=reservation.duration,
            payment_type=reservation.payment_type or 'cash',
            price=reservation.price,
            qr_code=reservation.qr_code
        )

        reservation.place.is_available = True
        reservation.place.save()
        reservation.delete()

        messages.success(request, f"Reservation {reservation.ticket_id} validated and archived.")
        return redirect('reservation_list')

from client_app.models import History, Reservation
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from .decorators import staff_required

@staff_required
def validate_all_expired_reservations(request):
    now = timezone.now()

    # Only filter with end_time__lte directly (timezone-aware)
    expired_reservations = Reservation.objects.filter(end_time__lte=now)

    count = 0
    for reservation in expired_reservations:
        History.objects.create(
            ticket_id=reservation.ticket_id,
            client=reservation.client,
            place=reservation.place,
            vehicule_type=reservation.vehicule_type,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            duration=reservation.duration,
            payment_type=reservation.payment_type or 'cash',
            price=reservation.price,
            qr_code=reservation.qr_code
        )

        reservation.place.is_available = True
        reservation.place.save()
        reservation.delete()
        count += 1

    if count == 0:
        messages.info(request, "ℹ️ No expired reservations found.")
    else:
        messages.success(request, f"✅ {count} reservation(s) validated and moved to history.")
    return redirect('reservation_list')


@staff_required
def history_view(request):
    history = History.objects.all().order_by('-end_time')
    total = history.count()
    return render(request, 'employee_app/history.html', {
        'histories': history,
        'total_past': total
    })


