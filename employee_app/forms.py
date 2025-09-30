from django import forms
from client_app.models import ParkingPlace, Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['place', 'vehicule_type', 'client_cin', 'payment_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place'].queryset = ParkingPlace.objects.filter(is_available=True)
