#!/bin/bash

cd "$(dirname "$0")"
poetry run uvicorn src.main:app --host 0.0.0.0 --reload
