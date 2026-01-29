# Secure Notes API

A Flask-based REST API for managing personal notes with JWT authentication.

---

## Features

- User registration and login
- JWT-based authentication
- Secure logout using token revocation (blocklist)
- Create, read, update, and delete notes
- User-based authorization (users can access only their own notes)
- Swagger (OpenAPI) documentation for API testing

---

## Tech Stack

- Python
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- Marshmallow
- SQLite
- Flasgger (Swagger UI)

---

## Getting Started

## Project Structure

secure_notes_api/
├── app/
│ ├── auth/
│ ├── notes/
│ ├── models.py
│ ├── config.py
│ └── init.py
├── run.py
├── requirements.txt
└── README.md

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/secure_notes_api.git
cd secure_notes_api

## Getting Started

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the application
python run.py

### The API will be available at:

http://127.0.0.1:5000

## API Documentation

Swagger UI is available at:

http://127.0.0.1:5000/apidocs/

You can use Swagger to:
Register and login users
Authorize using JWT
Test all protected note endpoints

### Authentication Flow

1.Register a new user
2.Login to receive a JWT access token
3.Use the token in requests:
4.Authorization: Bearer <token>
5.Access protected note endpoints
6.Logout to revoke the token

### Notes
JWT access tokens are short-lived by default
After logout, revoked tokens cannot be reused
Each user can only access their own notes

### Future Improvements (Optional)
Refresh tokens
Pytest test suite
Database migrations (Flask-Migrate)
Docker support
