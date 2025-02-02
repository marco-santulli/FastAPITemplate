# FastAPI User Management Template

This template implements a secure user management system following best practices outlined in our development guidelines. It provides basic user authentication and management functionality with JWT token support.

## Project Structure

```
app/
├── alembic/                  # Database migrations
├── core/                     # Core application components
│   ├── config.py            # Configuration management
│   ├── security.py          # Security utilities
│   └── database.py          # Database connection management
├── models/                   # SQLAlchemy models
│   └── user.py              # User model definition
├── schemas/                  # Pydantic schemas
│   └── user.py              # User-related schemas
├── services/                 # Business logic
│   └── user_service.py      # User-related services
├── api/                     # API routes
│   └── v1/
│       ├── endpoints/       # API endpoints
│       │   └── users.py    # User-related endpoints
│       └── api.py          # API router configuration
├── tests/                   # Test files
├── main.py                  # Application entry point
└── requirements.txt         # Project dependencies

## Security Considerations

1. Environment Variables:
   - Never commit .env files to version control
   - Use .env.example as a template, but remove sensitive values
   - Store production credentials in a secure vault
   - Rotate secrets regularly

2. Database Security:
   - Use connection pooling for efficient and secure connections
   - Never expose database port to public internet
   - Use strong passwords and encryption
   - Regular security audits and updates

3. API Security:
   - All endpoints are protected with JWT authentication
   - Passwords are hashed using bcrypt
   - Rate limiting is implemented
   - CORS is configured for specific origins

## Setup Instructions

1. Clone the repository
2. Copy .env.example to .env and fill in your configuration:
```bash
cp .env.example .env
```

3. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Initialize the database:
```bash
alembic upgrade head
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000
API documentation is available at http://localhost:8000/docs

## Development Guidelines

1. Code Style:
   - Follow PEP 8
   - Use black for formatting
   - Run pylint for static analysis

2. Testing:
   - Write unit tests for all new features
   - Maintain test coverage above 80%
   - Run tests before committing

3. Git Workflow:
   - Use feature branches
   - Squash commits before merging
   - Write meaningful commit messages

## API Documentation

The API provides the following endpoints:

- POST /api/v1/users/register - Register new user
- POST /api/v1/users/login - Login user
- GET /api/v1/users/me - Get current user info
- PUT /api/v1/users/me - Update current user info

## License

MIT License - See LICENSE file for details