# Statify Backend - Claude AI Instructions

## Project Overview
Statify is a multi-tenant real-time status page system for organizations to monitor services, log incidents, and show live status to end users. This is the FastAPI backend.

## Tech Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Auth**: JWT with bcrypt password hashing
- **Validation**: Pydantic v2 schemas
- **Real-time**: WebSocket connections for live updates
- **Containerization**: Docker & docker-compose

## Project Structure
```
backend/
├── app/
│   ├── controllers/    # Request handlers (business logic orchestration)
│   ├── services/       # Business logic and database operations
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic validation schemas
│   ├── routes/         # API route definitions
│   ├── middleware/     # Request middleware (auth, org context)
│   ├── utils/          # Utilities (auth, websocket, pubsub)
│   ├── core/           # Core config (event loop)
│   └── database.py     # Database connection
├── alembic/            # Database migrations
├── main.py             # FastAPI app entry point
└── requirements.txt
```

## Architecture Pattern
Routes -> Controllers -> Services -> Models

- **Routes**: Define API endpoints and request/response schemas
- **Controllers**: Orchestrate service calls, handle HTTP exceptions
- **Services**: Business logic, database queries
- **Models**: SQLAlchemy ORM definitions

## Development Commands
```bash
# Start with Docker
docker-compose up --build

# Local development
pip install -r requirements.txt
pip install -r dev-requirements.txt
uvicorn main:app --reload

# Database migrations
alembic upgrade head
alembic revision --autogenerate -m "description"
```

## Environment Variables
Requires `.env` file (see `.env.sample`):
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing secret
- `ALGORITHM` - JWT algorithm (HS256)

## API Endpoints

### Auth (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout (requires auth)
- `GET /auth/current_user` - Get current user

### Services (`/services`)
- `GET /services` - List org services
- `POST /services` - Create service
- `PUT /services/{id}` - Update service
- `DELETE /services/{id}` - Delete service

### Incidents (`/incidents`)
- CRUD for incident management
- Incident updates with status tracking

### Organizations
- Multi-tenant support with org-based filtering

## Code Conventions
- Use Pydantic schemas for all request/response validation
- Use `model_dump()` to convert Pydantic models to dict
- Return consistent responses via controller layer
- All models use UUID primary keys for multi-tenant isolation
- Org context extracted from request state middleware

## Multi-Tenancy
- Organization ID extracted from subdomain/header in middleware
- All queries filtered by org_id at service layer
- WebSocket broadcasts scoped to org_id

## Real-time Updates
- WebSocket manager handles connections per org
- `publish_ws_event()` broadcasts to all org connections
- Dead connections cleaned up automatically

## Testing
```bash
pytest
```

## Common Tasks

### Adding a New Model
1. Create SQLAlchemy model in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Create service in `app/services/`
4. Create controller in `app/controllers/`
5. Create routes in `app/routes/`
6. Register routes in `app/__init__.py`
7. Generate migration: `alembic revision --autogenerate`

### Adding a New Endpoint
1. Define Pydantic request/response schemas
2. Add service method with business logic
3. Add controller method with error handling
4. Add route with proper decorators

## API Documentation
Auto-generated Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`
