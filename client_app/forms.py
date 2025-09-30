# client_app/forms.py

from io import BytesIO
from tkinter import Canvas
from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponse

Client = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = Client
        fields = ['full_name', 'email']  # <- match field names exactly

    def save(self, commit=True):
        client = super().save(commit=False)
        client.set_password(self.cleaned_data['password'])
        if commit:
            client.save()
        return client
    
# client_app/forms.py

from django import forms
from .models import ParkingPlace
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['place', 'vehicule_type', 'start_time', 'end_time', 'payment_type']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place'].queryset = ParkingPlace.objects.filter(is_available=True)

# client_app/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ReservationForm
from .models import Reservation

@login_required
def book_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user  # Assign logged-in client
            reservation.save()  # Will trigger all logic in save() method
            
            # Mark the parking place as occupied
            reservation.place.is_available = False
            reservation.place.save()
            
            return redirect('reservation_success')  # Make this page later
    else:
        form = ReservationForm()
    return render(request, 'client_app/book_reservation.html', {'form': form})

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

@login_required
def download_ticket(request):
    try:
        reservation = Reservation.objects.filter(client=request.user).latest('id')
    except ObjectDoesNotExist:
        raise Http404("No reservation found for this user.")

    from reportlab.pdfgen import canvas  # ⬅️ fix for wrong import!
    buffer = BytesIO()
    p = canvas.Canvas(buffer)  # ← you had Canvas.Canvas (wrong!)

    p.setFont("Helvetica", 12)

    p.drawString(100, 800, "🎫 Parking Reservation Ticket")
    p.drawString(100, 770, f"Reservation ID: {reservation.ticket_id}")
    p.drawString(100, 750, f"Client: {reservation.client.full_name}")
    p.drawString(100, 730, f"Email: {reservation.client.email}")
    p.drawString(100, 710, f"Parking Spot: {reservation.place.number}")
    p.drawString(100, 690, f"Vehicle Type: {reservation.vehicule_type}")
    p.drawString(100, 670, f"Start: {reservation.start_time.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, 650, f"End: {reservation.end_time.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, 630, f"Duration: {reservation.duration} hours")
    p.drawString(100, 610, f"Total Price: ${reservation.price}")
    p.drawString(100, 590, f"Payment Type: {reservation.payment_type or 'N/A'}")

    p.showPage()
    p.save()
    buffer.seek(0)

    filename = f"reservation_{reservation.ticket_id}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

