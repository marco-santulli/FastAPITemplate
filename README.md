
# FastAPI Template Project

## Overview

This is a template project for FastAPI, designed based on best practices. It includes:
- User authentication with JWT token generation and verification.
- Database integration using PostgreSQL and SQLAlchemy.
- Modular structure for easy scalability and maintainability.

## Project Structure

```
app/
├── main.py                # Entry point of the application
├── routers/               # API route definitions
│   └── auth.py            # Authentication endpoints
├── models/                # Database models
│   └── user.py            # User model
├── schemas/               # Pydantic schemas for validation
│   └── user_schema.py     # Schemas for user requests and responses
├── services/              # Business logic layer
│   └── user_service.py    # User-related operations
├── core/                  # Core utilities and configurations
│   ├── config.py          # App and database configuration
│   └── security.py        # Security utilities (password hashing, JWT)
tests/
└── test_users.py          # Test cases for user routes
```

## Requirements

- Python 3.7+
- PostgreSQL
- pip for managing dependencies

## Setup

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone <repository-url>
   cd fastapi-template-project
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file for environment variables by copying `.env.example`:

   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your database credentials and secret key.

6. Run the database migrations (if using Alembic):

   ```bash
   alembic upgrade head
   ```

7. Start the application:

   ```bash
   uvicorn app.main:app --reload
   ```

## Running Tests

Run the test suite using pytest:

```bash
pytest
```

## Features

- **JWT Authentication**: Secure token-based authentication for user login.
- **PostgreSQL Integration**: Using SQLAlchemy for ORM.
- **Validation with Pydantic**: Strong typing and validation for API requests and responses.
- **Modular Structure**: Clean separation of concerns for scalability.

## API Endpoints

- `POST /auth/login`: Authenticate a user and receive a JWT token.

## Additional Notes

- Ensure your `.env` file is configured for sensitive data like `DATABASE_URL` and `SECRET_KEY`.
- Customize the project as needed to fit your application requirements.
