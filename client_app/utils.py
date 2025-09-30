# client_app/utils.py
from .models import Reservation, History
from django.utils.timezone import now

def archive_expired_reservations():
    expired_reservations = Reservation.objects.filter(end_time__lt=now())

    for reservation in expired_reservations:
        # Move to History
        History.objects.create(
            ticket_id=reservation.ticket_id,
            client=reservation.client,
            place=reservation.place,
            vehicule_type=reservation.vehicule_type,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            duration=reservation.duration,
            price=reservation.price,
            payment_type=reservation.payment_type,
            qr_code=reservation.qr_code  # Copy QR image reference
        )

        # Free up the place
        reservation.place.is_available = True
        reservation.place.save()

        # Delete original reservation
        reservation.delete()
