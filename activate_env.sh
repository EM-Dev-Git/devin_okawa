#!/bin/bash


VENV_PATH=$(poetry env info --path)
source "$VENV_PATH/bin/activate"
echo "Poetry virtual environment activated. You can now run:"
echo "uvicorn src.main:app --host 0.0.0.0 --reload"
