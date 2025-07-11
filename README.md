# Basic FastAPI Application

A simple FastAPI application following the official "First Steps" tutorial.

## Setup

1. Install dependencies:
   ```bash
   poetry install
   ```

2. Run the development server:
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   **Alternative: Using Poetry wrapper**
   ```bash
   poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
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

## Environment Variables

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

Key environment variables:
- `APP_NAME`: Application name (default: "FastAPI Basic Application")
- `DEBUG`: Enable/disable debug mode (default: true)
- `HOST`: Server host (default: "127.0.0.1")
- `PORT`: Server port (default: 8000)
- `SECRET_KEY`: Application secret key
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)

## Logging

The application includes comprehensive logging functionality:

- **Startup/Shutdown**: Application lifecycle events are logged
- **Endpoint Access**: All API endpoint calls are logged with INFO level
- **Error Handling**: Exceptions are logged with ERROR level
- **Log Format**: Timestamp, module name, level, and message
