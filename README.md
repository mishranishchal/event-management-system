# event-management-system
An event management system (EMS) is a centralized digital tool that streamlines and automates the planning, execution, and analysis of events.
# Event Management System — README

A Django-based web application for managing college fests, competitions, workshops, and related activities. This README gives a step-by-step setup guide (development and production), common commands, configuration examples, and tips for extending the app.

---

# Quick summary

* **Purpose:** Create and manage events, register participants, manage organisers/judges, send notifications, and run competitions.
* **Stack:** Django (backend)

---

# Quick start (development)

1. **Clone the repo**

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. **Create virtual environment & install**

```bash
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Create `.env`**

Copy `.env.example` (if present) to `.env` and fill required values. Example keys are shown below in the `Environment variables` section.

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Create a superuser**

```bash
python manage.py createsuperuser
```

6. **Run the dev server**

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

# Prerequisites

* Python 3.10+ (or supported version for your project)
* pip

---

# Environment variables (example)

Create a `.env` with at least:

---

# Database & migrations

* Use PostgreSQL in production. For development, SQLite is fine but behaviour (concurrency, JSON fields) differs.
* When you change models: `python manage.py makemigrations` then `python manage.py migrate`.
* To load sample data: `python manage.py loaddata sample_fixture.json` (if provided).

---

# Production checklist & deployment notes

* Set `DEBUG=False` and configure `ALLOWED_HOSTS`.
* Use a secure `SECRET_KEY` loaded from env.
* Serve static files with `collectstatic` and use WhiteNoise or a CDN/S3.

```bash
python manage.py collectstatic --noinput
```
---

# Key features (what this app usually includes)

* Event creation & editing (title, description, schedule, venue, capacity)
* Categories / tracks for contests
* Participant registration & team management
* Organizer / judge role management and dashboards
* Automated emails (confirmation, reminders)
* Result management and leaderboard
* File uploads (submissions) and size validation

---

# Useful management commands

* `python manage.py createsuperuser`
* `python manage.py migrate`
* `python manage.py makemigrations`
* `python manage.py collectstatic`
* `python manage.py loaddata <fixture.json>`
* `python manage.py test` (run test suite)
* Install `django-extensions` and run `python manage.py show_urls` to list all routes.

---

# Testing

* Unit tests: `python manage.py test`
* For APIs, use Postman / httpie or `pytest` + `pytest-django` if configured.

---

# Common troubleshooting

* **500 on deployment** -> Check logs, missing env variables, DEBUG=False misconfiguration.
* **Static files not found** -> Run `collectstatic` and configure static serving.
* **Email not sending** -> Verify SMTP credentials and ports.
* **Database connection errors** -> Confirm `DATABASE_URL` and that Postgres is running and accepting connections.


# Extending the app / tips

* Add background tasks (Celery) for email reminders and heavy report generation.
* Use Django signals carefully (avoid heavy work inside signals; offload to Celery).
* Add unit tests for critical flows: registration, payment, scoring.
* Use role-based permissions (`django-guardian` or DRF permissions) for fine-grained access.
