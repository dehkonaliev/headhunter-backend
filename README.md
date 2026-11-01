# Head-Hunter API

A REST API backend for a job marketplace that connects **employers** and **job seekers**. The platform supports company profiles, vacancies, resumes, job applications, and direct messaging between companies and candidates.

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.18-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Data Model](#data-model)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Roles and Permissions](#roles-and-permissions)
- [Response Format](#response-format)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development Notes](#development-notes)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

Head-Hunter API is a Django + Django REST Framework service organized as a set of domain apps:

- **Employers** register, create a company profile, publish vacancies, review applications, and chat with candidates.
- **Employees** build a structured resume (education, experience, skills, languages), browse vacancies, apply, and chat with companies.
- **Authentication** uses a two-step email verification flow followed by JWT access and refresh tokens.
- **API documentation** is available through Swagger UI and ReDoc.

The API is designed around role-based access control: each account is either an `EMPLOYEE` or an `EMPLOYER`, and permissions are enforced per endpoint.

---

## Features

- Email verification and account activation flow
- JWT authentication with refresh-token rotation and blacklisting
- Custom user profiles with avatars and thumbnails
- Company profiles with verification status
- Vacancy publishing with skills, categories, salary ranges, and employment types
- Structured resumes with education, experience, languages, and skills
- Job applications with status transitions
- Real-time-ready chat domain with typed messages (message, application, interview, archive)
- Admin back office via Django Admin
- Swagger and ReDoc API documentation
- Multipart image uploads for avatars, logos, and media
- Shared response envelope for consistent client handling

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.13 |
| Framework | Django 6.1.1 |
| API | Django REST Framework 3.18.1 |
| Authentication | `djangorestframework-simplejwt` 5.5.1 |
| Filtering | `django-filter` 26.2 |
| Documentation | `drf-yasg` (Swagger/ReDoc), `drf-spectacular` installed |
| Database | SQLite (development default) |
| Configuration | `python-dotenv` |
| Images | Pillow |
| Production drivers available | `psycopg2-binary`, `whitenoise`, `dj-database-url` |

---

## Architecture

The project follows a modular Django app layout:

| App | Responsibility |
| --- | --- |
| `core` | Project settings, root URL configuration, WSGI/ASGI entry points |
| `baseapp` | Abstract base model, reference data (`Region`, `District`, `Skill`, `Lang`, `Category`), shared permissions, validators, response helpers |
| `authentication` | Custom user model, temporary users, verification tokens, JWT login/logout, profiles |
| `companies` | Company profiles and admin verification |
| `vacancies` | Vacancy creation, listing, editing, and deletion |
| `resumes` | Resume builder: education, experience, languages, and skills |
| `applications` | Job applications and status workflow |
| `chat` | Conversations and messages between employees and companies |

### Design conventions

- All primary domain models inherit from `baseapp.models.BaseModel` and use UUID primary keys with `created_at` timestamps.
- Permissions are centralized in `baseapp/permissions.py` and `applications/permissions.py`.
- Validation helpers live in `baseapp/utils.py`, including name, username, and password rules.
- API responses use shared `success_response()` and `error_response()` helpers with a consistent JSON envelope.

---

## Data Model

### Core entities

| Model | Key relationships | Description |
| --- | --- | --- |
| `CustomUser` | extends `AbstractUser` | Role-aware account with profile fields |
| `TempUser` | — | Pending email verification with expiring code |
| `MyToken` | `TempUser` | One-time token used to complete registration |
| `Company` | `CustomUser` (employer) | Company profile with verification flag |
| `Vacancy` | `Company`, `Category`, `District`, `Skill` | Job posting with salary range and status |
| `Resume` | `CustomUser` (employee) | Candidate profile, one per employee |
| `Education` | `Resume` | Education history entries |
| `Experience` | `Resume` | Work experience entries |
| `Language` | `Resume`, `Lang` | Language proficiency entries |
| `Application` | `Vacancy`, `Resume` | Job application with status workflow |
| `Chat` | `CustomUser`, `Company` | Conversation thread between a candidate and a company |
| `Message` | `Chat`, `Application` | Chat message or application event |

### Reference data

`Region`, `District`, `Skill`, `Lang`, and `Category` are managed through Django Admin and must be populated before creating vacancies or resumes.

### Application status workflow

```
new -> viewed -> interview
new -> discard
viewed -> interview
viewed -> discard
```

Applications that reach `interview` cannot be withdrawn by the candidate.

---

## API Reference

All endpoints are relative to the server root, for example `http://127.0.0.1:8000`.

**Legend:** Public = no token required | Employee = `EMPLOYEE` role required for writes | Employer = `EMPLOYER` role required for writes | Auth = any authenticated user.

### Authentication

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `POST` | `/api/auth/signup` | Public | Create a temporary user and generate a verification code |
| `POST` | `/api/auth/verify-code` | Public | Verify the email code and receive a registration token |
| `POST` | `/api/auth/create-account` | Public | Complete registration using the verification token |
| `POST` | `/api/auth/login` | Public | Obtain JWT access and refresh tokens |
| `POST` | `/api/auth/logout` | Auth | Blacklist a refresh token |
| `POST` | `/api/auth/token/refresh` | Public | Rotate an expired access token |
| `GET` | `/api/auth/get-user` | Public | Return the current role, or `anonymous` |
| `GET` | `/api/auth/profile` | Auth | Retrieve the authenticated user's profile |
| `PATCH` | `/api/auth/profile` | Auth | Update the authenticated user's profile |

### Resumes

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/api/resumes/resume` | Employee | Get the current user's resume |
| `POST` | `/api/resumes/resume` | Employee | Create a resume (one per employee) |
| `PATCH` | `/api/resumes/resume` | Employee | Update the current user's resume |
| `GET` | `/api/resumes/resume-get/<uuid>` | Employee | Get a resume by ID (private resumes restricted to owner) |
| `PATCH` | `/api/resumes/skills` | Employee | Add skills to the resume |
| `DELETE` | `/api/resumes/skills` | Employee | Remove skills from the resume |
| `POST` | `/api/resumes/education-add` | Employee | Add an education entry |
| `PATCH` | `/api/resumes/education/<uuid>` | Employee | Update an education entry |
| `DELETE` | `/api/resumes/education/<uuid>` | Employee | Delete an education entry |
| `POST` | `/api/resumes/experience-add` | Employee | Add a work experience entry |
| `PATCH` | `/api/resumes/experience/<uuid>` | Employee | Update a work experience entry |
| `DELETE` | `/api/resumes/experience/<uuid>` | Employee | Delete a work experience entry |
| `POST` | `/api/resumes/language-add` | Employee | Add a language entry |
| `PATCH` | `/api/resumes/language/<uuid>` | Employee | Update a language entry |
| `DELETE` | `/api/resumes/language/<uuid>` | Employee | Delete a language entry |

### Vacancies

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/api/vacancies/vacancy-list-create` | Public | List active vacancies |
| `POST` | `/api/vacancies/vacancy-list-create` | Employer | Create a vacancy |
| `GET` | `/api/vacancies/vacancy/<uuid>` | Public | Retrieve an active vacancy |
| `PATCH` | `/api/vacancies/vacancy/<uuid>` | Employer (owner) | Update a vacancy |
| `DELETE` | `/api/vacancies/vacancy/<uuid>` | Employer (owner) | Delete a vacancy |
| `GET` | `/api/vacancies/my-vacancies` | Employer | List vacancies owned by the current employer |
| `GET` | `/api/vacancies/my-vacancy/<uuid>` | Employer | Retrieve one of the current employer's vacancies, including drafts |

### Chat

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| `GET` | `/api/chats/chat-list` | Employee | List the current candidate's conversations |
| `POST` | `/api/chats/message` | Auth | Send a message in a chat |
| `GET` | `/api/chats/chat-messages/<uuid>` | Auth (participant) | List messages in a conversation |
| `PATCH` | `/api/chats/message/<uuid>` | Auth (sender) | Edit an owned message |
| `DELETE` | `/api/chats/message/<uuid>` | Auth (sender) | Delete an owned message |

### Documentation and admin

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/docs/swagger/` | Swagger UI |
| `GET` | `/api/docs/redoc/` | ReDoc UI |
| `GET` | `/api/docs/swagger<format>/` | Schema without UI (for example `.json`) |
| `GET` | `/admin/` | Django Admin |

> **Note:** The `companies` and `applications` URL configurations exist but are not currently mounted in `core/urls.py`. Their views are implemented and can be enabled by uncommenting the corresponding `include(...)` entries.

---

## Authentication Flow

```
1. POST /api/auth/signup          { "email": "user@example.com" }
2. POST /api/auth/verify-code     { "email": "user@example.com", "code": 123456 }
                                  -> { "token": "<registration-token>" }
3. POST /api/auth/create-account  { "token": "<registration-token>", "username": "...",
                                     "first_name": "...", "last_name": "...",
                                     "user_role": "EMPLOYEE", "password": "...",
                                     "conf_password": "..." }
4. POST /api/auth/login           { "username": "...", "password": "..." }
                                  -> access + refresh tokens
5. Send the access token in the Authorization header:
   Authorization: Bearer <access-token>
6. POST /api/auth/token/refresh   { "refresh": "<refresh-token>" }
7. POST /api/auth/logout          { "refresh": "<refresh-token>" }
```

### Token lifecycle

- Access tokens expire after **100 minutes**.
- Refresh tokens expire after **7 days**.
- Refresh tokens rotate on use.
- Rotated tokens are blacklisted, so old refresh tokens cannot be reused.

### Registration rules

- Email addresses must be unique across active users.
- Verification codes expire after **15 minutes**.
- Usernames are 3–50 characters, alphanumeric or underscore, and cannot start with a digit.
- Passwords must contain uppercase, lowercase, numeric, and special characters.
- `user_role` must be `EMPLOYEE` or `EMPLOYER`.

> In development, the email backend writes to the console and the verification code generator does not send email yet. Retrieve pending codes from the Django Admin or the database during local testing.

---

## Roles and Permissions

| Role | Capabilities |
| --- | --- |
| `EMPLOYEE` | Manage a resume and its sections, browse vacancies, apply to jobs, chat with companies |
| `EMPLOYER` | Manage a company, publish and manage vacancies, review applications, chat with candidates |
| Anonymous | Read-only access to public data such as active vacancies and profiles |
| Staff / superuser | Django Admin, company verification |

Permission classes used across the project:

- `IsEmployee` / `IsEmployeeStrict` — employee-only writes
- `IsEmployer` — employer-only writes, read-only for others
- `IsOwnerOrReadOnly` / `IsOwnerStrict` — object ownership checks
- `IsVacancyOwner` — employer ownership of a vacancy

---

## Response Format

Successful response:

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "tokens": {
      "access": "<access-token>",
      "refresh": "<refresh-token>"
    }
  }
}
```

Error response:

```json
{
  "success": false,
  "message": "Invalid username or password.",
  "data": null
}
```

Validation errors follow DRF conventions and are returned with HTTP `400`.

### Status codes

| Code | Meaning |
| --- | --- |
| `200` | Success |
| `201` | Resource created |
| `204` | Resource deleted |
| `400` | Validation error |
| `401` | Authentication required or token invalid |
| `403` | Permission denied |
| `404` | Resource not found |

---

## Getting Started

### Prerequisites

- Python **3.13+**
- `pip`
- Git

### Installation

```bash
git clone https://github.com/dehkonaliev/02_pro.git
cd 02_pro/backend
```

Create and activate a virtual environment:

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If script execution is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Create a `.env` file inside `backend/`:

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-string
```

Generate a suitable key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

### Database setup

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000`.

### Seed reference data

Before creating vacancies or resumes, add reference records through Django Admin (`/admin/`):

- Regions and districts
- Skills
- Languages
- Categories

### Quick verification

```bash
curl http://127.0.0.1:8000/api/vacancies/vacancy-list-create
```

---

## Environment Variables

The project loads `backend/.env` via `python-dotenv`.

| Variable | Required | Description |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Yes | Django cryptographic signing key |

Additional settings currently use development defaults in `core/settings.py`. For production, move secrets and configuration such as `DEBUG`, `ALLOWED_HOSTS`, database credentials, and email settings into environment variables.

---

## API Documentation

Start the development server and open:

- Swagger UI: [http://127.0.0.1:8000/api/docs/swagger/](http://127.0.0.1:8000/api/docs/swagger/)
- ReDoc: [http://127.0.0.1:8000/api/docs/redoc/](http://127.0.0.1:8000/api/docs/redoc/)

You can authorize requests in Swagger using a JWT access token.

---

## Project Structure

```
Head-Hunter/
├── README.md
└── backend/
    ├── manage.py
    ├── requirements.txt
    ├── db.sqlite3
    ├── .env
    ├── core/                  # Settings, URLs, WSGI/ASGI
    ├── baseapp/               # Base model, reference data, utilities, permissions
    ├── authentication/        # Custom user, verification, JWT, profile
    ├── companies/             # Company profiles (routes not mounted)
    ├── vacancies/             # Vacancy management
    ├── resumes/               # Resume builder
    ├── applications/          # Job applications (routes not mounted)
    └── chat/                  # Conversations and messages
```

Each domain app follows the same layout: `models.py`, `serializers.py`, `views.py`, `urls.py`, `admin.py`, `permissions.py` (where needed), `tests.py`, and `migrations/`.

---

## Development Notes

- **Database:** SQLite is the default for local development. `psycopg2-binary` and `dj-database-url` are installed, so switching to PostgreSQL is straightforward.
- **Media files:** Uploaded images are stored under `backend/media/` and served by Django when `DEBUG=True`.
- **Pagination:** Where enabled, page size is 20. Vacancy, resume, and chat list endpoints currently return unpaginated results.
- **Filtering:** Company endpoints support `django-filter`, search, and ordering when mounted.
- **Testing:** `tests.py` files are present but contain no test cases yet. Run the suite with `python manage.py test`.
- **Requirements encoding:** On Windows, `requirements.txt` may be UTF-16 encoded. If `pip` reports invalid requirements, convert it first:

  ```powershell
  Get-Content .\requirements.txt -Raw | Set-Content .\requirements.txt -Encoding utf8
  ```

### Before deploying to production

- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- Use a strong `DJANGO_SECRET_KEY`
- Replace SQLite with PostgreSQL
- Configure a real email backend and wire verification-code delivery
- Collect static files and serve them with WhiteNoise or a reverse proxy
- Add rate limiting, logging, and automated tests

---

## Roadmap

- Mount the `companies` and `applications` routers
- Expose the `drf-spectacular` OpenAPI schema alongside Swagger/ReDoc
- Enforce company verification before chat creation
- Add resume/vacancy search, filtering, and pagination
- Add automated API tests and CI checks
- Add WebSocket-based chat delivery
- Add Docker and deployment configuration

---

## License

No license file is currently included in this repository. Contact the maintainer for usage terms.

**Maintainer:** [@dehkonaliev](https://github.com/dehkonaliev)
