# FastAPI Meeting Minutes Generator - Startup Guide

## Quick Start

### Method 1: Using Startup Scripts (Recommended)
```bash
# For production-like setup
./start_app.sh

# For development
./start_dev.sh
```

### Method 2: Manual Startup
```bash
# Activate virtual environment
source venv/bin/activate

# Start with uvicorn (recommended)
uvicorn src.main:app --reload

# Alternative with PYTHONPATH
PYTHONPATH=. python src/main.py
```

## Environment Configuration

### Default Development Values
The application includes safe defaults for development:
- `AZURE_OPENAI_API_KEY`: test_key_for_development
- `AZURE_OPENAI_ENDPOINT`: https://test.openai.azure.com/
- `JWT_SECRET_KEY`: test_secret_key_for_development_only_change_in_production

### Production Setup
For production, create a `.env` file with real values:
```bash
cp .env.example .env
# Edit .env with your actual values
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"
- **Cause**: Running from wrong directory or missing PYTHONPATH
- **Solution**: Use uvicorn or set PYTHONPATH=.

### "Field required" validation errors
- **Cause**: Missing environment variables (fixed in this version)
- **Solution**: Use provided defaults or set up .env file

### "Address already in use"
- **Cause**: Another server is running on port 8000
- **Solution**: Kill existing process or use different port

## API Endpoints
- Root: http://localhost:8000/
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs
- Authentication: http://localhost:8000/api/v1/auth/
- Minutes: http://localhost:8000/api/v1/minutes/
