# ParClick
ParClick – Smart Parking Management in Django: QR tickets, client reservations, employee validation, and history tracking.

ParClick is a full-stack Django application that streamlines parking reservations for clients and operational oversight for employees. It features real-time availability, QR-code tickets, automated pricing, and an employee dashboard for validation and history tracking.

- Live QR-tickets for entry/validation
- Time-based pricing for cars and motorcycles
- Client self-service booking and history
- Employee dashboard for managing places, reservations, and validation

## ✨ Features

- Client UX
  - Browse available places and make reservations
  - Instant price estimation based on duration and vehicle type
  - Download QR code ticket
  - Manage and cancel reservations
  - View reservation history

- Employee UX
  - Secure login and session-based access
  - Dashboard for active reservations
  - Validate tickets (by ticket id / time checks)
  - Manage parking places and release/occupy slots
  - Historical view of completed reservations

- Core
  - QR code generation (`qrcode`, `Pillow`)
  - PDF/print-ready tickets (via `reportlab`, optional)
  - Media storage for QR assets
  - SQLite by default; easily switch to Postgres
  - Django 5.2, Bootstrap 5 landing page

## 🧱 Architecture

- `client_app`: client-facing auth, reservation booking, history
- `employee_app`: employee auth, dashboard, validation, place management
- `parclick`: project config, global templates

Key models:
- `ParkingPlace(number, is_available)`
- `Reservation(client, place, vehicule_type, start_time, end_time, duration, price, payment_type, qr_code)`
- `History(...)` for completed reservations

Note: The repo includes separate `Client` and `Employee` models. In a production setup, you’d typically consolidate to a single `User` with a `role` field. This project keeps them separate to showcase role-specific workflows.

## 🚀 Quickstart

Prerequisites:
- Python 3.10+
- pip / venv

Setup:
```bash
git clone <your-fork-or-repo-url>
cd parclick
python -m venv env
env\Scripts\activate  # Windows
pip install -r requirements.txt

# env
copy .env.example .env  # fill values (optional for local)
# DB + media
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# seed demo data (optional)
python manage.py create_parking_places
python manage.py create_employee
python manage.py runserver
```

Visit:
- Landing: http://127.0.0.1:8000/
- Client: http://127.0.0.1:8000/client/home/
- Employee: http://127.0.0.1:8000/employee/login/

## 🔐 Environment

Create `.env` (see `.env.example`):
- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL` (optional, for Postgres)
- `MEDIA_ROOT`, `STATIC_ROOT` (deployment)

## 📸 Screenshots

Place images in `docs/screenshots/` and reference them here:
- Landing page
- Client reservation form
- QR ticket
- Employee dashboard

Example:
```markdown
![Welcome](docs/screenshots/welcome.png)
![Reservation](docs/screenshots/reservation.png)
![Dashboard](docs/screenshots/dashboard.png)
```

## 🧪 Tests (suggested)

- Ticket uniqueness
- Price calculation (car vs motorcycle)
- Reservation time validation
- Cancelation releases parking place
- Employee validation flow

Run:
```bash
python manage.py test
```

## 🛣️ Roadmap

- Consolidate auth to single `User(role=CLIENT|EMPLOYEE)`
- Prevent double-booking with transactional locks
- Add REST API and SPA frontend (React/Vue)
- Add payment gateway
- Add CI (lint, test) and Dockerfile

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs welcome!

## 🛡️ Security

If you discover a vulnerability, please see [SECURITY.md](SECURITY.md).

## 📄 License

MIT – see [LICENSE](LICENSE).

---
Built with Django 5.2, Bootstrap 5, and a lot of green buttons.

<img width="709" height="515" alt="Screenshot 2025-09-16 233144" src="https://github.com/user-attachments/assets/0f8be874-006f-426c-a502-7e5c50cb71f8" />

<img width="730" height="590" alt="Screenshot 2025-09-16 233158" src="https://github.com/user-attachments/assets/74ed4fa2-e5b9-46ee-aa60-fd7851d15cd7" />

<img width="1759" height="957" alt="Screenshot 2025-09-16 233337" src="https://github.com/user-attachments/assets/0ac42454-f118-467e-855a-36551595f1f6" />

<img width="1758" height="957" alt="Screenshot 2025-09-16 233426" src="https://github.com/user-attachments/assets/2ef36970-e536-4c83-99cb-c1b00aab67e1" />

<img width="1756" height="951" alt="Screenshot 2025-09-16 233911" src="https://github.com/user-attachments/assets/1e859bf5-0056-4a13-a89d-c44259aeee34" />

<img width="1759" height="796" alt="Screenshot 2025-09-16 234014" src="https://github.com/user-attachments/assets/f7fdd22f-a9fe-4d1f-b059-a2eb5145bd71" />

<img width="1758" height="842" alt="Screenshot 2025-09-16 234037" src="https://github.com/user-attachments/assets/bb21ce56-e0da-48d6-84e0-fefec0732606" />

<img width="1691" height="951" alt="Screenshot 2025-09-30 125709" src="https://github.com/user-attachments/assets/1e1935ec-4564-4069-ab80-bd4bea323c26" />

<img width="1759" height="952" alt="Screenshot 2025-09-30 125726" src="https://github.com/user-attachments/assets/efdf1f95-fd6b-4f2f-890e-06bdbcf866db" />

<img width="1759" height="956" alt="Screenshot 2025-09-30 125737" src="https://github.com/user-attachments/assets/5af80d44-2eda-48bc-8cde-974df85c802a" />

<img width="1759" height="953" alt="Screenshot 2025-09-16 235357" src="https://github.com/user-attachments/assets/67763162-9e95-4209-b763-a65be831d2ec" />











