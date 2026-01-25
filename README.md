# Health Tracker App

A full-stack web application for tracking nutrition and managing health goals.

## Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Profile Management**: Track personal information (age, gender, height, weight, activity level)
- **Nutrition Tracking**: Log food intake with calories and macronutrients
- **Daily Summary**: View daily nutrition totals and progress

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: MariaDB 10.11.15
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT with bcrypt password hashing
- **Testing**: pytest with 70% coverage minimum

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State Management**: React Context API

## Project Structure

```
health-tracker-app/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── routes/       # API endpoints
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── alembic/          # Database migrations
│   ├── tests/            # Test suite
│   └── requirements.txt  # Python dependencies
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── context/      # React Context
│   │   └── services/     # API clients
│   └── package.json      # Node dependencies
└── .github/workflows/    # CI/CD pipelines
```

## Setup

### Backend Setup

1. Create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API URL
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The app will be available at http://localhost:3000

## Testing

### Backend Tests

Run tests with coverage:
```bash
cd backend
pytest --cov=app --cov-report=term-missing
```

### Code Quality

Run linting:
```bash
black app tests
flake8 app tests --max-line-length=100
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### Testing Environment
- API: https://healthapi.gahfaudio.in
- Frontend: https://health.gahfaudio.in

### Production Environment
- API: https://healthapi.gahfaudio.in
- Frontend: https://health.gahfaudio.in

## License

MIT
