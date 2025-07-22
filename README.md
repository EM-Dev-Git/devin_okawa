# Meeting Minutes Generator

FastAPI-based Azure OpenAI powered meeting minutes generation system with session-based authentication.

## Setup Instructions

### 1. Environment Configuration

Copy the environment template and configure your settings:

```bash
cp env/.env.example env/.env
```

Edit `env/.env` with your actual configuration:

```env
# Azure OpenAI API設定
azure_openai_api_key=your_actual_azure_openai_api_key
azure_openai_model=gpt-4
azure_openai_version=2024-02-15-preview
azure_openai_endpoint=https://your-actual-resource.openai.azure.com/

# セッション認証設定
session_secret_key=your_actual_super_secret_session_key_change_in_production
session_expire_hours=24

# 認証除外パス設定
auth_excluded_paths=/api/v1/auth/login,/api/v1/auth/register,/api/v1/auth/logout,/login,/health
```

**Important:** 
- Replace `your_actual_azure_openai_api_key` with your Azure OpenAI API key
- Replace `your_actual_super_secret_session_key_change_in_production` with a strong, unique secret key
- The `env/.env` file is ignored by git and should never be committed

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at `http://localhost:8000`

## Authentication

The application uses session-based authentication to protect all endpoints except:
- `/health` - Health check endpoint
- `/api/v1/auth/login` - User login
- `/api/v1/auth/register` - User registration
- `/api/v1/auth/logout` - User logout

### First Time Setup

1. Register a new user:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "email": "your_email@example.com", "password": "your_password"}'
```

2. Login to create a session:
```bash
curl -c cookies.txt -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your_username&password=your_password"
```

3. Access protected endpoints with session:
```bash
curl -b cookies.txt -X GET "http://localhost:8000/"
```

## API Endpoints

- `GET /` - Root endpoint (protected)
- `GET /health` - Health check (public)
- `POST /api/v1/auth/register` - User registration (public)
- `POST /api/v1/auth/login` - User login (public)
- `POST /api/v1/auth/logout` - User logout (public)
- `POST /api/v1/minutes/generate` - Generate meeting minutes (protected)

## Development

The application uses in-memory user storage for development purposes. User data will be lost when the application restarts.

For production deployment, consider implementing persistent user storage.
