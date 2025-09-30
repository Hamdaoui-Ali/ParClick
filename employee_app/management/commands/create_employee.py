from django.core.management.base import BaseCommand
from employee_app.models import Employee

class Command(BaseCommand):
    help = "Create a test employee user for development."

    def handle(self, *args, **kwargs):
        email = 'ayman@gmail.com'
        password = 'ayman'
        employee_id = 'EMP1003'
        full_name = 'Ayman Yamani'
        employee_cin = '2232'
        employee_phone = '0633453916'

        if Employee.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"⚠️ Employee with email '{email}' already exists."))
            return

        employee = Employee.objects.create_user(
            email=email,
            password=password,
            employee_id=employee_id,
            full_name=full_name,
            employee_cin=employee_cin,
            employee_phone=employee_phone,
            is_staff=True  # Required to access staff views
        )

        self.stdout.write(self.style.SUCCESS(f"✅ Test employee created: {employee.email}"))
        self.stdout.write(self.style.SUCCESS(f"👉 Login with: {email} / {password}"))
