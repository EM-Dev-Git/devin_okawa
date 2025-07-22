# FastAPI Meeting Minutes Generator with OAuth2 Authentication

FastAPI議事録生成アプリケーション（OAuth2認証付き）

## Quick Start

### 1. Setup
```bash
# Clone repository
git clone <repository-url>
cd devin_okawa

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 2. Start Application
```bash
# Easy startup (recommended)
./start_app.sh

# Or manual startup
source venv/bin/activate
uvicorn src.main:app --reload
```

### 3. Access Application
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Environment Configuration
The application works out-of-the-box with development defaults. For production, copy `.env.example` to `.env` and configure with real values.

See [STARTUP_GUIDE.md](STARTUP_GUIDE.md) for detailed instructions.

## Features
- OAuth2 JWT authentication
- User registration and login
- Meeting minutes generation with Azure OpenAI
- Comprehensive test suite (90% coverage)
- Development-friendly configuration

## Testing
```bash
source venv/bin/activate
PYTHONPATH=. pytest
```

## Architecture
- FastAPI backend with async support
- Pydantic for data validation
- JWT-based authentication
- Azure OpenAI integration for AI-powered minutes generation
- In-memory user storage (development)
- Comprehensive error handling and logging
