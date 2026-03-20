# Incident Management - Backend

Django REST API for managing incidents. Users register, log in, and manage their own incidents. Nobody can see someone else's incidents. Once an incident is closed, it stays closed.

Pincode lookup is handled via the India Post API - enter a 6-digit Indian pincode and city, state, country fill in automatically.

Forgot password uses a 6-digit OTP. For now the OTP prints to the server console only.

---

## Getting started

Clone the repo and go into the backend folder:

```bash
git clone https://github.com/prachikush16/incident-backend.git
cd incident_management
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Database setup

Create the database and user in PostgreSQL:

```sql
CREATE DATABASE incident_db;
CREATE USER incident_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE incident_db TO incident_user;
```

---

## Environment variables

Create a `.env` file in the project root. All variables are listed below:

```

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SERVER_PORT=8005

DB_ENGINE=django.db.backends.postgresql
DB_NAME=incident_db
DB_USER=incident_user
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

JWT_ACCESS_TOKEN_LIFETIME_HOURS=1
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
OTP_EXPIRY_MINUTES=10

# India Post pincode API - used to auto-fill city, state, country from a 6-digit pincode
PINCODE_API_URL=https://api.postalpincode.in/pincode
PINCODE_API_TIMEOUT=5
PINCODE_API_USER_AGENT=Mozilla/5.0

```

---

## Running the project

Apply migrations:

```bash
python manage.py migrate
```

Create a superuser to access the admin panel:

```bash
python manage.py createsuperuser
```

Start the server:

```bash
python manage.py runserver 8005
```

Admin panel: `http://127.0.0.1:8005/admin/`

---

## API routes

**Users**

```
POST   /api/users/register/                    register a new user
POST   /api/users/login/                       login, get access + refresh tokens
POST   /api/users/token/refresh/               get a new access token using refresh token
GET    /api/users/profile/                     get logged-in user's profile
PATCH  /api/users/profile/                     update profile
GET    /api/users/pincode/<pincode>/            lookup city, state, country for a pincode
POST   /api/users/change-password/             change password (must be logged in)
POST   /api/users/forgot-password/send-otp/    send OTP to the registered email
POST   /api/users/forgot-password/verify-otp/  verify the OTP
POST   /api/users/forgot-password/reset/       reset password after OTP is verified
```

**Incidents**

```
GET    /api/incidents/                         list your incidents
POST   /api/incidents/                         create a new incident
GET    /api/incidents/<id>/                    view an incident
PATCH  /api/incidents/<id>/                    edit an incident (not allowed if closed)
GET    /api/incidents/search/?incident_id=     find an incident by its ID
GET    /api/incidents/autofill/                get your details to pre-fill the incident form
```

---
