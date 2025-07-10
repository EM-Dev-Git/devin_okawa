# Basic FastAPI Application

A simple FastAPI application following the official "First Steps" tutorial.

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run the development server:
   ```bash
   fastapi dev main.py
   ```

3. Open your browser at http://127.0.0.1:8000

## API Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

- `GET /` - Returns a simple "Hello World" message
- `GET /health` - Returns application health status
- `POST /items/` - Create a new item
- `GET /items/` - Get all items

## Project Structure

```
├── main.py              # FastAPI application entry point
├── routers/             # API route handlers
│   ├── root.py         # Root and health endpoints
│   └── items.py        # Items management endpoints
├── schemas/             # Pydantic models for request/response validation
│   ├── base.py         # Base response models
│   └── items.py        # Item-related schemas
├── modules/             # Business logic modules
│   ├── health.py       # Health check service
│   └── items.py        # Item management service
└── utils/               # Utility modules
    └── logger.py       # Centralized logging configuration
```

## Logging

The application includes comprehensive logging functionality:

- **Startup/Shutdown**: Application lifecycle events are logged
- **Endpoint Access**: All API endpoint calls are logged with INFO level
- **Error Handling**: Exceptions are logged with ERROR level
- **Log Format**: Timestamp, module name, level, and message
