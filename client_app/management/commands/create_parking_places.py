# client_app/management/commands/create_parking_places.py

from django.core.management.base import BaseCommand
from client_app.models import ParkingPlace

class Command(BaseCommand):
    help = 'Create 100 parking places (A1 to A100)'

    def handle(self, *args, **kwargs):
        created = 0
        for i in range(1, 101):
            number = f"A{i}"
            obj, was_created = ParkingPlace.objects.get_or_create(number=number)
            if was_created:
                obj.is_available = True
                obj.save()
                created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} parking places.'))
