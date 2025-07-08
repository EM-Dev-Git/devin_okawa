# Meeting Minutes Generation System (Test0)

This directory contains the complete meeting minutes generation system implementation.

## Overview

A system that converts transcription text into structured meeting minutes using AI summarization and multiple output formats.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. Start the server:
   ```bash
   uvicorn src.api.main:app --reload
   ```

4. Access the web UI at `http://localhost:8000`

## Features

- **Transcription Processing**: Parse and preprocess transcription text
- **AI Summarization**: Generate meeting summaries using OpenAI GPT-4
- **Multiple Output Formats**: HTML, Markdown, JSON, and PDF
- **Web UI**: User-friendly interface with file upload and text input
- **REST API**: FastAPI endpoints for integration

## Directory Structure

```
test0/
├── src/                    # Source code
│   ├── api/               # FastAPI application
│   ├── transcription/     # Text processing
│   ├── ai/               # AI summarization
│   └── minutes/          # Output generation
├── config/               # Configuration
├── templates/            # HTML templates
├── sample_data/          # Test data
├── tests/               # Unit tests
├── requirements.txt     # Dependencies
└── .env.example        # Environment template
```

## Testing

Run basic functionality tests:
```bash
python test_basic_functionality.py
```

## Original Implementation

This code was developed as part of the meeting minutes generation system project.
