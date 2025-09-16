#!/usr/bin/env bash
set -euo pipefail

# Python venv + deps
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
if [ -f backend/requirements.txt ]; then pip install -r backend/requirements.txt; fi

# Frontend deps
if [ -f frontend/package.json ]; then cd frontend && npm install && cd -; fi