# Health Tracker Frontend

React frontend for the Health Tracker application.

## Features

- User authentication (login/register)
- Protected routes for authenticated pages
- Profile management
- Food log entry and management
- Daily nutrition dashboard

## Pages

- `/login` - Login page
- `/register` - Registration page
- `/` - Dashboard (protected)
- `/food-log` - Food log management (protected)
- `/profile` - User profile (protected)

## Components

- `Navbar` - Navigation bar with auth state
- `ProtectedRoute` - Route wrapper for authentication
- `FoodLogCard` - Card component for food log entries

## Context

- `AuthContext` - Global authentication state management

## Services

- `authService` - Authentication API calls
- `profileService` - Profile management API calls
- `nutritionService` - Nutrition tracking API calls

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests

## Environment Variables

Create a `.env` file based on `.env.example`:

```
REACT_APP_API_URL=http://localhost:8000
```
