#!/bin/bash

check_env_file() {
    if [ ! -f .env ]; then
        echo "⚠️  .env file not found!"
        echo "Please copy .env.example to .env and configure your settings:"
        echo "  cp .env.example .env"
        echo ""
        echo "Continuing with development defaults..."
        sleep 2
    else
        echo "✓ .env file found"
    fi
}

echo "Starting FastAPI Meeting Minutes Generator..."
check_env_file
source venv/bin/activate
echo "Virtual environment activated"
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
