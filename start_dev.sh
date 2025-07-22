#!/bin/bash
echo "Starting development server..."
source venv/bin/activate
echo "Virtual environment activated"
uvicorn src.main:app --reload
