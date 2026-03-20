# Whisper Transcription Tool

## Overview
This project is a transcription platform built using OpenAI Whisper, designed to process audio files and generate accurate text transcriptions through an asynchronous and scalable architecture.

It combines a FastAPI backend, background processing with Redis and RQ, and a containerized environment for easy deployment and development.

## Features
- Audio-to-text transcription using Whisper
- Asynchronous processing with job queue (Redis + RQ)
- REST API for managing transcription jobs
- Support for multiple models, devices, and formats
- Scalable and containerized architecture (Docker)
- Ready for production deployment (VPS setup)

## Tech Stack
- Python
- FastAPI
- OpenAI Whisper / Faster-Whisper
- Redis + RQ (background jobs)
- PostgreSQL
- Docker & Docker Compose

## How it works
1. Upload an audio file via the API  
2. A background job is created and processed asynchronously  
3. The transcription result is stored and can be retrieved via API  

## Quick start (development)

Start services:
    docker compose up -d

Run API manually (optional):
    uvicorn backend.app.main:app --reload

API available at:  
http://localhost:8000

## Example

    curl -F "file=@sample.wav" http://localhost:8000/transcriptions

## Purpose of the project
This project was built as a personal initiative to explore AI-driven transcription, asynchronous processing, and scalable backend architectures.

As a Technical Project Manager with a software engineering background, I actively develop projects like this to stay hands-on with modern technologies and better understand the systems I lead.

## Documentation

Detailed documentation is available in the `/docs` folder:

- Application setup (production): `docs/app-setup.md`
- Developer setup: `docs/developer-setup.md`
- Backend API: `docs/backend.md`
- Services and infrastructure: `docs/services.md`
- Database: `docs/database.md`
- Roadmap: `docs/roadmap.md`

## Future improvements
- Batch processing for multiple audio files
- Language detection and translation
- Export formats (SRT, VTT)
- Web UI enhancements
- Authentication and user management

---
