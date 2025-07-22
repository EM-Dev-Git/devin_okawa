#!/bin/bash
echo "Starting FastAPI Meeting Minutes Generator..."
source venv/bin/activate
echo "Virtual environment activated"
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
