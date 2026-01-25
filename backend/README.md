# Health Tracker Backend

FastAPI backend for the Health Tracker application.

## Features

- User authentication with JWT
- User profile management
- Food log CRUD operations
- Daily nutrition summary

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Profile
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update user profile

### Nutrition
- `POST /api/nutrition/food-log` - Create food log entry
- `GET /api/nutrition/food-log` - List food logs
- `GET /api/nutrition/food-log/{id}` - Get specific food log
- `PUT /api/nutrition/food-log/{id}` - Update food log
- `DELETE /api/nutrition/food-log/{id}` - Delete food log
- `GET /api/nutrition/daily-summary` - Get daily nutrition summary

## Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `password_hash`: Bcrypt hashed password
- `name`, `age`, `gender`, `height_cm`, `weight_kg`, `activity_level`: Profile fields
- `created_at`, `updated_at`: Timestamps

### Food Logs Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `food_name`: Name of food
- `calories`, `protein_g`, `carbs_g`, `fats_g`: Nutrition values
- `logged_at`: When the food was consumed
- `created_at`, `updated_at`: Timestamps

## Running Tests

```bash
pytest --cov=app --cov-report=term-missing --cov-fail-under=70
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```
