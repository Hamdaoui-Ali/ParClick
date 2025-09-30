from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import get_user_model

Client = get_user_model()

def login_register_view(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return render(request, 'client_app/home.html')

                else:
                    messages.error(request, "Invalid email or password")

        elif 'register_submit' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                client = register_form.save(commit=False)
                client.set_password(register_form.cleaned_data['password'])
                client.save()
                login(request, client)
                return render(request, 'client_app/home.html')

            else:
                messages.error(request, "Registration error. Please fix the form.")

    return render(request, 'client_app/login_register.html', {
        'login_form': login_form,
        'register_form': register_form
    })
    
    # client_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Client, Reservation
from .forms import LoginForm, RegisterForm

def client_auth(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)
                    return render(request, 'client_app/home.html')

        elif 'signup' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'client_app/home.html')

    else:
        form = LoginForm()
        signup_form = RegisterForm()
    return render(request, 'client_app/login_signup.html', {
        'login_form': LoginForm(),
        'signup_form': RegisterForm()
    })

from .utils import archive_expired_reservations
@login_required
def home(request):
    archive_expired_reservations()  # Archive if any expired
    return render(request, 'client_app/home.html')

def client_logout(request):
    logout(request)
    return redirect('client_login')

from django.contrib.auth.decorators import login_required

@login_required
def reservation_success(request):
    return render(request, 'client_app/reservation_success.html')

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(client=request.user).order_by('-start_time')
    return render(request, 'client_app/my_reservations.html', {'reservations': reservations})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, client=request.user)
    
    # Make the place available again
    reservation.place.is_available = True
    reservation.place.save()

    # Delete the reservation
    reservation.delete()

    return redirect('my_reservations')

@login_required
def about_page(request):
    return render(request, 'client_app/about.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from client_app.models import History

@login_required
def client_history_view(request):
    user = request.user
    history = History.objects.filter(client=user).order_by('-end_time')
    return render(request, 'client_app/history.html', {'history': history})