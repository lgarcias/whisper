FROM mcr.microsoft.com/devcontainers/python:3.11

# System deps for audio & builds
RUN apt-get update \
    && apt-get install -y ffmpeg git curl build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Node.js 20 (for frontend)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Optional: Redis CLI
RUN apt-get update && apt-get install -y redis-tools && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/whisper-website

# Crea las carpetas de caché y ajusta permisos
RUN mkdir -p /models/whisper /models/hf /models/cache && \
    chown -R vscode:vscode /models
